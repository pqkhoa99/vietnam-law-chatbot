import re
import json
from enum import Enum
from loguru import logger
from vietnam_law_chatbot.core.config import settings
from vietnam_law_chatbot.core.prompts import CHUNKING_SYSTEM_PROMPT, PARSING_RELATIONSHIP_PROMPT

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
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        
        # System prompt for LLM parsing
        self.CHUNKING_SYSTEM_PROMPT = CHUNKING_SYSTEM_PROMPT
        self.PARSING_RELATIONSHIP_PROMPT = PARSING_RELATIONSHIP_PROMPT

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

        first_type = ""
        for lines in content.splitlines():
            if lines.strip().startswith("Chương") or lines.strip().startswith("Mục") or lines.strip().startswith("Điều"):
                first_type = lines.strip().split()[0]
                break
    
        if chuong_matches and (first_type == "Chương"):
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
                    chuong_content = chuong[2].replace(chuong_data["title"], "", 1).strip()
                else:
                    chuong_data["title"] = ""
                    chuong_content = chuong[2].strip()

                first_type = chuong_content.strip().split()[0] if chuong_content.strip() else ""
                muc_matches = muc_regex.findall(chuong_content)
                if muc_matches and (first_type == "Mục"):
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
                            muc_content = muc[1].replace(muc_data["title"], "", 1).strip()
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
            muc_matches = muc_regex.findall(content)
            if muc_matches and (first_type == "Mục"):
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
                        muc_content = muc[1].replace(muc_data["title"], "", 1).strip()
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

                    data.append(muc_data)
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
            model=settings.OPENAI_PARSE_MODEL,
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

    def chunking_articles(self, document_data: dict) -> dict:
        """
        Chunks the document content into articles based on the 'Điều' prefix.

        Args:
            document_data (dict): Dictionary from the crawler containing document content and info.

        Returns:
            dict: A dictionary containing the parsed information.
        """
        if not document_data:
            return {}
        
        data = document_data.get("data", [])
        if not data:
            return {}
        
        articles = []
        
        dieu_regex_number = re.compile(r'Điều\s*([0-9]+)')
        
        for first_level in data:
            if first_level.get("type") == VBPLSection.CHAPTER.name:
                for section in first_level.get("children", []):
                    if section.get("type") == VBPLSection.SECTION.name:
                        for article in section.get("children", []):
                            if article.get("type") == VBPLSection.ARTICLE.name:
                                article["document_id"] = document_data.get("document_info", {}).get("document_id", "")
                                article["id"] = document_data.get("document_info", {}).get("document_id", "") + "_" + dieu_regex_number.search(article["content"]).group(1)
                                article["chapter"] = first_level.get("id_text", "") + ": " + first_level.get("title", "")
                                article["section"] = section.get("id_text", "") + ": " + section.get("title", "")
                                articles.append(article)
                    else:
                        section["document_id"] = document_data.get("document_info", {}).get("document_id", "")
                        section["id"] = document_data.get("document_info", {}).get("document_id", "") + "_" + dieu_regex_number.search(section["content"]).group(1)
                        section["chapter"] = first_level.get("id_text", "") + ": " + first_level.get("title", "")
                        section["section"] = None
                        articles.append(section)
            elif first_level.get("type") == VBPLSection.SECTION.name:
                for article in first_level.get("children", []):
                    if article.get("type") == VBPLSection.ARTICLE.name:
                        article["document_id"] = document_data.get("document_info", {}).get("document_id", "")
                        article["id"] = document_data.get("document_info", {}).get("document_id", "") + "_" + dieu_regex_number.search(article["content"]).group(1)
                        article["chapter"] = None
                        article["section"] = first_level.get("id_text", "") + ": " + first_level.get("title", "")
                        articles.append(article)
            else:
                if first_level.get("type") == VBPLSection.ARTICLE.name:
                    first_level["document_id"] = document_data.get("document_info", {}).get("document_id", "")
                    first_level["id"] = document_data.get("document_info", {}).get("document_id", "") + "_" + dieu_regex_number.search(first_level["content"]).group(1)
                    first_level["chapter"] = None
                    first_level["section"] = None
                    articles.append(first_level)

        # Multithreaded chunking
        def chunk_article(article):
            """
            Helper function to chunk a single article using the OpenAI client.
            """
            relationship = document_data.get("document_info", {}).get("relationship", {})
            relationship = json.dumps(relationship, ensure_ascii=False, indent=2)
            relationship = re.sub(r'\([\s\S]+?\)', '', relationship)
            content = f"""
                <current_document_id>{document_data.get("document_info", {}).get("document_id", {})}</current_document_id>
                <document_metadata>
                {relationship}
                </document_metadata>
                <article_content>
                {article['content']}
                </article_content>
            """.strip()
            try:
                response = self.openai_client.chat.completions.create(
                    model=settings.OPENAI_PARSE_MODEL,
                    messages=[
                        {"role": "system", "content": self.PARSING_RELATIONSHIP_PROMPT},
                        {"role": "user", "content": content}
                    ],
                    temperature=0.5,
                )
                response_text = response.choices[0].message.content.replace('```json', '').replace('```', '')
                response_text = re.sub(r'(<think>[\s\S]+?</think>)|(<thinking>[\s\S]+?</thinking>)', '', response_text).strip()
                logger.debug(f"Response text for article {article['id']}: {response_text}")
                response_json = json.loads(response_text)
                article["Sửa đổi, bổ sung"] = response_json.get("Sửa đổi, bổ sung", [])
                article["Thay thế"] = response_json.get("Thay thế", [])
                article["Bãi bỏ"] = response_json.get("Bãi bỏ", [])
                article["Đình chỉ việc thi hành"] = response_json.get("Đình chỉ việc thi hành", [])
                article["Hướng dẫn, quy định"] = response_json.get("Hướng dẫn, quy định", [])
                article["external"] = response_json.get("external", [])

                return article

            except Exception as e:
                logger.error(f"Error chunking article {article['id']}: {e}")
                return None
            
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        tasks = []
        with ThreadPoolExecutor(max_workers=settings.CONCURRENCY_LIMIT) as executor:
            for article in articles:
                tasks.append(executor.submit(chunk_article, article))

        parsed_articles = []
        for future in as_completed(tasks):
            result = future.result()
            if result:
                parsed_articles.append(result)

        return parsed_articles
