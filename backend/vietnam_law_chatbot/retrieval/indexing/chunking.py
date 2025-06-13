import re
import json
import unicodedata
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

    def parse_helper(self, content, section_name: VBPLSection):
            """
            Helper function to process content with a regex pattern.
            Args:
                content (str): The content to process.
                section_name (VBPLSection): The section name to match against.
            Returns:
                list: A list of matches found in the content.
            """
            lines = content.splitlines()
            parsed_data = []
            current_number = 0
            chunk = ""
            inquote = 0
            if section_name == VBPLSection.ARTICLE:
                for line in lines:
                    if current_number == 0 and re.match(rf"^\s*{VBPLSection.ARTICLE.value}\s*[0-9]+\s*\.", line.strip()):
                        chunk = line
                        current_number = int(re.search(r'\d+', line).group(0))
                        continue
                    if re.match(rf"^\s*{VBPLSection.ARTICLE.value}\s*{current_number + 1}\s*\.", line.strip()):
                        # if chunk and chunk.startswith(VBPLSection.ARTICLE.value):
                        if chunk and re.match(rf"^\s*{VBPLSection.ARTICLE.value}\s*{current_number}\s*\.", chunk.strip()):
                            parsed_data.append(chunk)
                        chunk = line
                        current_number += 1
                    else:
                        chunk += "\n" + line if chunk else line
                if chunk:
                    parsed_data.append(chunk)
            elif section_name == VBPLSection.CLAUSE:
                for line in lines:
                    # Replace smart quotes with regular quotes
                    line = line.replace('“', '"')
                    line = line.replace('”', '"')
                    line = line.replace('‘', '"')
                    line = line.replace('’', '"')
                    
                    # Count quotes to determine if we are in a quote
                    inquote += line.count('"')
                    if inquote % 2 == 0:
                        inquote = 0
                        
                    if current_number == 0 and re.match(rf"^\s*[0-9]+\s*\.", line.strip()):
                        chunk = line
                        current_number = int(re.search(r'\d+', line).group(0))
                        continue
                    if re.match(rf"^\s*{current_number + 1}\s*\.", line.strip()) and inquote == 0:
                        if chunk and re.match(rf"^\s*{current_number}\s*\.", chunk.strip()):
                            parsed_data.append(chunk)
                        chunk = line
                        current_number += 1
                    else:
                        chunk += "\n" + line if chunk else line

                if chunk:
                    if parsed_data:
                        parsed_data.append(chunk)
                    else:
                        current_number = 1
                        for line in lines:
                            if not re.match(rf"^\s*{VBPLSection.ARTICLE.value}\s*[0-9]+\s*\.", line.strip()) and line.strip():
                                parsed_data.append(f"{current_number}. {line.strip()}")
                                current_number += 1
            else:
                logger.error(f"Unsupported section name: {section_name}")
            return parsed_data

    def convert_to_id(self, text: str) -> str:
        """
        Converts a text to a valid ID by removing special characters and replacing spaces with underscores.

        Args:
            text (str): The text to convert.

        Returns:
            str: A valid ID string.
        """
        if not text:
            return ""
        # Normalize the text
        normalized_text = unicodedata.normalize('NFC', text)
        # Convert to lowercase
        normalized_text = normalized_text.lower()
        # Make it to English, remove accents
        vietnamese_map = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'đ': 'd',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
        }
        normalized_text = ''.join(vietnamese_map.get(char, char) for char in normalized_text)
        # Remove special characters except underscores and alphanumeric characters
        normalized_text = re.sub(r'[^\w\s]', '', normalized_text)
        # Remove multiple spaces
        normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()
        
        if ' ' not in normalized_text and not normalized_text.isdigit():
            prefixes = ["Chương", "Mục", "Điều"]
            for p in prefixes:
                if normalized_text.startswith(p):
                    normalized_text = normalized_text.replace(p, "").strip()
                    break
            id_text = f"{p}-{normalized_text}"
        elif normalized_text.isdigit():
            id_text = f"khoan-{normalized_text}"
        else:
            # Replace spaces with underscores
            id_text = normalized_text.replace(' ', '-')
            # Remove any leading or trailing underscores
            id_text = id_text.strip('-')

        return id_text
    
    def title_parser(self, title: str) -> str:
        """
        Parses the title of a document to remove unwanted characters and normalize it.

        Args:
            title (str): The title to parse.

        Returns:
            str: A cleaned and normalized title.
        """
        lines = title.splitlines()
        title = ""
        for i, line in enumerate(lines):
            if not re.match(r'^\s*(Mục|Điều)\s*[0-9]+', line.strip()):
                title += line
            else:
                lines = lines[i:]
                break

        title = re.sub(r'\s+', ' ', title).strip()
        return re.sub(r'[#*_\[\]\(\)-]', '', title).strip(), '\n'.join(lines).strip()

    
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
            
        content = unicodedata.normalize('NFC', document_data.get("text_content", ""))
        if not content:
            return {}

        # Clean up the content
        data = []
        chuong_regex = re.compile(r'\n*\s*(Chương\s*([MDCLXVI]+))\s*([\s\S]*?)(?=(\n+\s*Chương\s*([MDCLXVI]+))|\Z)')
        muc_regex = re.compile(r'\n*\s*(Mục\s*[0-9]+)([\s\S]+?)(?=(\n+\s*Mục\s*[0-9]+)|(\n+\s*Chương\s*([MDCLXVI]+))|\Z)')

        chuong_matches = chuong_regex.findall(content)

        first_type = ""
        for lines in content.splitlines():
            if lines.strip().startswith("Chương") or lines.strip().startswith("Mục") or lines.strip().startswith("Điều"):
                first_type = lines.strip().split()[0]
                break
    
        if chuong_matches and (first_type == "Chương"):
            for chuong in chuong_matches:
                title, chuong_content = self.title_parser(chuong[2].strip())
                chuong_data = {
                    "type": VBPLSection.CHAPTER.name,
                    "id": self.convert_to_id(chuong[0].strip()),
                    "id_text": chuong[0].strip(),
                    "title": title,
                    "content": chuong_content,
                    "children": []
                }
                
                first_type = chuong_content.strip().split()[0] if chuong_content.strip() else ""
                muc_matches = muc_regex.findall(chuong_content)
                if muc_matches and (first_type == "Mục"):
                    for muc in muc_matches:
                        title, muc_content = self.title_parser(muc[1].strip())
                        muc_data = {
                            "type": VBPLSection.SECTION.name,
                            "id": f"{self.convert_to_id(muc[0].strip())}_{chuong_data['id']}",
                            "id_text": muc[0].strip(),
                            "title": title,
                            "content": muc_content,
                            "children": []
                        }

                        dieu_matches = self.parse_helper(muc_content, VBPLSection.ARTICLE)

                        for dieu in dieu_matches:
                            dieu_id = f"{self.convert_to_id(dieu.strip().split('.', 1)[0].strip())}_{muc_data['id']}"
                            dieu_data = {
                                "id": dieu_id,
                                "id_text": dieu.strip().split('.', 1)[0],
                                "title": re.search(r'^\s*Điều\s*[0-9]+\.\s*(.+)', dieu).group(1),
                                "type": VBPLSection.ARTICLE.name,
                                "content": dieu.replace('*', '').strip(),
                                "children": [
                                    {
                                        "id": f"{self.convert_to_id(clause.split('.', 1)[0])}_{dieu_id}",
                                        "id_text": clause.strip().split()[0].replace('.', ''),
                                        "type": VBPLSection.CLAUSE.name,
                                        "content": clause.strip()
                                    } for clause in self.parse_helper(dieu, VBPLSection.CLAUSE)
                                ]
                            }
                            muc_data["children"].append(dieu_data)

                        chuong_data["children"].append(muc_data)
                        
                    data.append(chuong_data)
                else:
                    dieu_matches = self.parse_helper(chuong_content, VBPLSection.ARTICLE)
                    if dieu_matches:
                        for dieu in dieu_matches:
                            dieu_id = f"{self.convert_to_id(dieu.strip().split('.', 1)[0].strip())}_{chuong_data['id']}"
                            dieu_data = {
                                "id": dieu_id,
                                "id_text": dieu.strip().split('.', 1)[0],
                                "title": re.search(r'^\s*Điều\s*[0-9]+\.\s*(.+)', dieu).group(1),
                                "type": VBPLSection.ARTICLE.name,
                                "content": dieu.replace('*', '').strip(),
                                "children": [
                                    {
                                        "id": f"{self.convert_to_id(clause.split('.', 1)[0])}_{dieu_id}",
                                        "id_text": clause.strip().split()[0].replace('.', ''),
                                        "type": VBPLSection.CLAUSE.name,
                                        "content": clause.strip()
                                    } for clause in self.parse_helper(dieu, VBPLSection.CLAUSE)
                                ]
                            }
                            chuong_data["children"].append(dieu_data)
                    data.append(chuong_data)
        else:
            muc_matches = muc_regex.findall(content)
            if muc_matches and (first_type == "Mục"):
                for muc in muc_matches:
                    title, muc_content = self.title_parser(muc[1].strip())
                    muc_data = {
                        "type": VBPLSection.SECTION.name,
                        "id": self.convert_to_id(muc[0].strip()),
                        "id_text": muc[0].strip(),
                        "title": title,
                        "content": muc_content,
                        "children": []
                    }
                    
                    dieu_matches = self.parse_helper(muc_content, VBPLSection.ARTICLE)

                    for dieu in dieu_matches:
                        dieu_id = f"{self.convert_to_id(dieu.strip().split('.', 1)[0].strip())}_{muc_data['id']}"
                        dieu_data = {
                            "id": dieu_id,
                            "id_text": dieu.strip().split('.', 1)[0],
                            "title": re.search(r'^\s*Điều\s*[0-9]+\.\s*(.+)', dieu).group(1),
                            "type": VBPLSection.ARTICLE.name,
                            "content": dieu.replace('*', '').strip(),
                            "children": [
                                {
                                    "id": f"{self.convert_to_id(clause.split('.', 1)[0])}_{dieu_id}",
                                    "id_text": clause.strip().split()[0].replace('.', ''),
                                    "type": VBPLSection.CLAUSE.name,
                                    "content": clause.strip()
                                } for clause in self.parse_helper(dieu, VBPLSection.CLAUSE)
                            ]
                        }
                        muc_data["children"].append(dieu_data)

                    data.append(muc_data)
            else:
                dieu_matches = self.parse_helper(content, VBPLSection.ARTICLE)

                if dieu_matches:
                    for dieu in dieu_matches:
                        dieu_id = f"{self.convert_to_id(dieu.strip().split('.', 1)[0].strip())}"
                        dieu_data = {
                            "id": dieu_id,
                            "id_text": dieu.strip().split('.', 1)[0],
                            "title": re.search(r'^\s*Điều\s*[0-9]+\.\s*(.+)', dieu).group(1),
                            "type": VBPLSection.ARTICLE.name,
                            "content": dieu.replace('*', '').strip(),
                            "children": [
                                {
                                    "id": f"{self.convert_to_id(clause.split('.', 1)[0])}_{dieu_id}",
                                    "id_text": clause.strip().split()[0].replace('.', ''),
                                    "type": VBPLSection.CLAUSE.name,
                                    "content": clause.strip()
                                } for clause in self.parse_helper(dieu, VBPLSection.CLAUSE)
                            ]
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
        def chunk_article(article, retries=3):
            """
            Helper function to chunk a single article using the OpenAI client.
            """
            relationship = document_data.get("document_info", {}).get("relationship", {})
            relationship.pop("Văn bản HD, QĐ chi tiết", None)
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
                removed_thinking = re.sub(r'(<think>[\s\S]*</think>)|(<thinking>[\s\S]*</thinking>)', '', response.choices[0].message.content)
                json_regex = re.compile(r'\{[\s\S]*\}')
                response_text = json_regex.search(removed_thinking).group(0)
                response_json = json.loads(response_text)
                logger.debug(f"Chunked article {article['id']} with raw response: {response.choices[0].message.content}")
                logger.debug(f"Parsed article {article['id']} with response: {response_json}")
                article["Sửa đổi, bổ sung"] = response_json.get("Sửa đổi, bổ sung", [])
                article["Thay thế"] = response_json.get("Thay thế", [])
                article["Bãi bỏ"] = response_json.get("Bãi bỏ", [])
                article["Đình chỉ việc thi hành"] = response_json.get("Đình chỉ việc thi hành", [])
                article["Hướng dẫn, quy định"] = response_json.get("Hướng dẫn, quy định", [])
                article["external"] = response_json.get("external", [])
                if article["external"]:
                    external = []
                    for ext in response_json["external"]:
                        if isinstance(ext, dict):
                            for key, value in ext.items():
                                if key != article["id"]:
                                    external.append({key: value})
                                else:
                                    logger.warning(f"Article {article['id']} has external reference to itself, overwriting.")
                                    article["Sửa đổi, bổ sung"] = value.get("Sửa đổi, bổ sung", [])
                                    article["Thay thế"] = value.get("Thay thế", [])
                                    article["Bãi bỏ"] = value.get("Bãi bỏ", [])
                                    article["Đình chỉ việc thi hành"] = value.get("Đình chỉ việc thi hành", [])
                                    article["Hướng dẫn, quy định"] = value.get("Hướng dẫn, quy định", [])

                    article["external"] = external

                return article

            except Exception as e:
                logger.error(f"Error chunking article {article['id']}: {e} | Response: {response.choices[0].message.content}")
                if retries > 0:
                    logger.info(f"Retrying chunking article {article['id']}: {retries} retries left")
                    return chunk_article(article, retries - 1)
                else:
                    logger.error(f"Failed to chunk article {article['id']} after retries")
                article["Sửa đổi, bổ sung"] = []
                article["Thay thế"] = []
                article["Bãi bỏ"] = []
                article["Đình chỉ việc thi hành"] = []
                article["Hướng dẫn, quy định"] = []
                article["external"] = []
                return article
            
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
