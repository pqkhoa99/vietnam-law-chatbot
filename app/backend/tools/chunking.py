import re
import json
from enum import Enum
from loguru import logger
from core.prompts import CHUNKING_SYSTEM_PROMPT

class VBPLSection(Enum):
    """
    Enum representing different sections of a legal document.
    """
    CHAPTER = "Chương"
    SECTION = "Mục"
    ARTICLE = "Điều"
    CLAUSE = "Khoản"
    POINT = "Điểm"
    SUBPOINT = "Mục con"

class VBPLChunker:
    """
    A class to chunk and parse legal documents from crawled data.
    """
    def __init__(self, openai_client=None, settings=None):
        self.openai_client = openai_client
        self.settings = settings
        
        # System prompt for LLM parsing
        self.CHUNKING_SYSTEM_PROMPT = CHUNKING_SYSTEM_PROMPT

    def chunking_by_prefix(self, document_data: dict) -> dict:
        """
        Chunks the document content based on prefixes like Chương, Mục, Điều.

        Args:
            document_data (dict): Dictionary from the crawler containing document content and info.

        Returns:
            dict: A dictionary containing the parsed information.
        """
        if not document_data:
            return {}
            
        content = document_data.get("text_content", "")
        if not content:
            return {}

        # Clean up the content
        data = []
        title_regex = re.compile(r'([\s\S]+?)(?=(\n+\s*Điều\s*[0-9]+)|(\n+\s*Mục\s*[0-9]+))', re.IGNORECASE)
        chuong_regex = re.compile(r'\n*\s*(Chương\s*([MDCLXVI]+))\s*([\s\S]*?)(?=(\n+\s*Chương\s*([MDCLXVI]+))|\Z)')
        muc_regex = re.compile(r'\n*\s*(Mục\s*[0-9]+)([\s\S]+?)(?=(\n+\s*Mục\s*[0-9]+)|(\n+\s*Chương\s*([MDCLXVI]+))|\Z)')
        dieu_regex = re.compile(r'\n*\s*(Điều\s*[0-9]*\\*\.+[\s\S]+?)(?=\n+\s*Điều\s*[0-9]+\\*\.|\Z)')

        chuong_matches = chuong_regex.findall(content)
        if chuong_matches:
            for chuong in chuong_matches:
                chuong_data = {
                    "type": VBPLSection.CHAPTER.name,
                    "id_text": chuong[0].strip(),
                    "title": "",
                    "children": []
                }
                
                title_match = title_regex.search(chuong[2])
                if title_match:
                    chuong_data["title"] = re.sub(r'\s+', ' ', re.sub(r'[#*_\[\]\(\)-]', '', title_match.group(0))).strip()
                    chuong_content = chuong[2].replace(chuong_data["title"], "").strip()
                else:
                    chuong_data["title"] = ""
                    chuong_content = chuong[2].strip()

                muc_matches = muc_regex.findall(chuong_content)
                if muc_matches:
                    for muc in muc_matches:
                        muc_data = {
                            "type": VBPLSection.SECTION.name,
                            "id_text": muc[0].strip(),
                            "title": "",
                            "children": []
                        }
                        
                        title_match = title_regex.search(muc[1])
                        if title_match:
                            muc_data["title"] = re.sub(r'\s+', ' ', re.sub(r'[#*_\[\]\(\)-]', '', title_match.group(0))).strip()
                            muc_content = muc[1].replace(muc_data["title"], "").strip()
                        else:
                            muc_data["title"] = ""
                            muc_content = muc[1].strip()

                        dieu_matches = dieu_regex.findall(muc_content)

                        for dieu in dieu_matches:
                            dieu_data = {
                                "type": VBPLSection.ARTICLE.name,
                                "content": dieu.replace('*', '').strip(),
                            }
                            muc_data["children"].append(dieu_data)

                        chuong_data["children"].append(muc_data)
                        
                    data.append(chuong_data)
                else:
                    dieu_matches = dieu_regex.findall(chuong_content)
                    if dieu_matches:
                        for dieu in dieu_matches:
                            dieu_data = {
                                "type": VBPLSection.ARTICLE.name,
                                "content": dieu.replace('*', '').strip(),
                            }
                            chuong_data["children"].append(dieu_data)
                    data.append(chuong_data)
        else:
            # Check dieu
            dieu_matches = dieu_regex.findall(content)
            if dieu_matches:
                for dieu in dieu_matches:
                    dieu_data = {
                        "type": VBPLSection.ARTICLE.name,
                        "content": dieu.replace('*', '').strip(),
                    }
                    data.append(dieu_data)

        # Create the final result dictionary
        dict_result = {
            "document_info": document_data.get("document_info", {}),
            "data": data
        }
        return dict_result

    def chunking_with_llm(self, document_data: dict) -> dict:
        """
        Chunks the document content using an LLM to extract relevant information.
        
        Args:
            document_data (dict): Dictionary from the crawler containing document content and info.

        Returns:
            dict: A dictionary containing the parsed information.
        """
        if not document_data or not self.openai_client:
            return {}
            
        content = document_data.get("text_content", "")
        if not content:
            return {}
        
        # Add line numbers to content
        content_lines = content.splitlines()
        modified_lines = []
        for i, line in enumerate(content_lines):
            modified_lines.append(f'{i+1} | {line.strip()}')

        modified_content = "\n".join(modified_lines)

        # Call the LLM for parsing
        response = self.openai_client.chat.completions.create(
            model=self.settings.OPENAI_MODEL if self.settings else "gpt-4",
            messages=[
                {"role": "system", "content": self.CHUNKING_SYSTEM_PROMPT},
                {"role": "user", "content": modified_content}
            ],
            temperature=0.8,
        )
        response_text = response.choices[0].message.content.replace('```json', '').replace('```', '').strip()

        try:
            response_json = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}")
            logger.error(f"Response text: {response_text}")
            return {}
        
        # Process the response to include full content
        for data in response_json:
            if data.get("type") == "ARTICLE":
                data["content"] = '\n'.join(content_lines[data["start_line"]-1:data["end_line"]]).strip()
                del data["start_line"]
                del data["end_line"]
            else:
                children = data.get("children", [])
                for child in children:
                    if child.get("type") == "ARTICLE":
                        child["content"] = '\n'.join(content_lines[child["start_line"]-1:child["end_line"]]).strip()
                        del child["start_line"]
                        del child["end_line"]
                    else:
                        for sub_child in child.get("children", []):
                            if sub_child.get("type") == "ARTICLE":
                                sub_child["content"] = '\n'.join(content_lines[sub_child["start_line"]-1:sub_child["end_line"]]).strip()
                                del sub_child["start_line"]
                                del sub_child["end_line"]
        
        return {
            "document_info": document_data.get("document_info", {}),
            "data": response_json,
        }
