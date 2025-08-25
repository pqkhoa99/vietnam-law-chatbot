import httpx
import html2text
import re
import time
import json
from loguru import logger
from bs4 import BeautifulSoup
from typing import List, Set, Tuple, Dict, Any

class VBPLCrawler:
    """
    A class to crawl legal documents from the Vietnam Government Portal (VBPL).
    """
    def __init__(self):
        self.toanvan_url = "https://vbpl.vn/nganhangnhanuoc/Pages/vbpq-toanvan.aspx?ItemID={}"
        self.luocdo_url = "https://vbpl.vn/nganhangnhanuoc/Pages/vbpq-luocdo.aspx?ItemID={}"
        self.categories = {
            'thong_tu': {'idLoaiVanBan': 22, 'name': 'Thông tư', 'max_pages': 75},
            'nghi_dinh': {'idLoaiVanBan': 3, 'name': 'Nghị định', 'max_pages': 50},
            'quyet_dinh': {'idLoaiVanBan': 9, 'name': 'Quyết định', 'max_pages': 100},
            'chi_thi': {'idLoaiVanBan': 6, 'name': 'Chỉ thị', 'max_pages': 30},
            'luat': {'idLoaiVanBan': 1, 'name': 'Luật', 'max_pages': 20},
            'phap_lenh': {'idLoaiVanBan': 2, 'name': 'Pháp lệnh', 'max_pages': 15},
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl_toanvan(self, id: str) -> str:
        """
        Crawls the given URL and returns the HTML content as a string.

        Args:
            id (str): The document ID to crawl toanvan page.

        Returns:
            str: The HTML content of the page.
        """
        try:
            response = httpx.get(self.toanvan_url.format(id), timeout=30)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ""
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            return ""
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return ""
    
    def crawl_luocdo(self, id: str) -> str:
        """
        Crawls the given URL and returns the HTML content as a string.

        Args:
            id (str): The document ID to crawl luocdo page.

        Returns:
            str: The HTML content of the page.
        """
        try:
            response = httpx.get(self.luocdo_url.format(id), timeout=30)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ""
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            return ""
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return ""
        
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parses the given HTML content and returns a BeautifulSoup object.

        Args:
            html (str): The HTML content to parse.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the parsed HTML.
        """
        return BeautifulSoup(html, 'html.parser')
    
    def extract_toanvancontent(self, soup: BeautifulSoup) -> str:
        """
        Extracts the full text from the parsed HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            str: The plain text extracted from the fulltext div.
        """
        fulltext_div = soup.find('div', class_='toanvancontent')
        if fulltext_div:
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text_maker.ignore_images = True
            return text_maker.handle(str(fulltext_div)).strip()
        return ""
    
    def extract_info(self, soup: BeautifulSoup) -> dict:
        """
        Extracts document information from the parsed HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            dict: A dictionary containing the document information.
        """
        info = {}

        vbInfo_div = soup.find('div', class_='vbInfo')
        if vbInfo_div:
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text_maker.ignore_images = True
            plain_text = text_maker.handle(str(vbInfo_div)).strip()
            lines = plain_text.split('\n')
            for line in lines:
                if "Hiệu lực: " in line:
                    info["document_status"] = line.split("Hiệu lực: ")[-1].strip()
                elif "Ngày có hiệu lực: " in line:
                    info["effective_date"] = line.split("Ngày có hiệu lực: ")[-1].strip()
                elif "Ngày hết hiệu lực: " in line:
                    info["expired_date"] = line.split("Ngày hết hiệu lực: ")[-1].strip()
                else:
                    pass
        
        boxmap_div = soup.find('div', class_='box-map')
        if boxmap_div:
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text_maker.ignore_images = True
            plain_text = text_maker.handle(str(boxmap_div)).strip()
            lines = plain_text.split('\n')
            info["document_title"] = lines[-1].replace('*', '').strip() if lines else ""

        header_div = soup.find('div', class_='header')
        if header_div:
            a_tag = header_div.find('a', class_='selected')
            if a_tag and 'href' in a_tag.attrs:
                info["document_id"] = a_tag['href'].split('ItemID=')[-1].split('&')[0].strip()
        
        relationship = {}
        html_luocdo = self.crawl_luocdo(info.get("document_id", "")) if info.get("document_id") else ""
        if html_luocdo:
            soup_luocdo = self.parse_html(html_luocdo)
            luocdo_div = soup_luocdo.find('div', class_='vbLuocDo')
            relationship = {}
            
            if luocdo_div:
                luocdo_children = luocdo_div.select('div[class^="luocdo"]')
                for child in luocdo_children:
                    # Get the title
                    child_title = child.find('div', class_='title') or child.find('div', class_='titleht')
                    if child_title:
                        # Extract the title text properly
                        title_text = ""
                        title_links = child_title.find_all('a')
                        for link in title_links:
                            if link.get('class') and 'openClose' in link.get('class'):
                                continue
                            title_link_text = link.get_text(strip=True)
                            if title_link_text:
                                title_text = title_link_text
                                break
                        
                        if title_text:
                            relationship[title_text] = []
                            
                            # Process content
                            content_div = child.find('div', class_='content')
                            if content_div:
                                list_items = content_div.find_all('li')
                                for li in list_items:
                                    # Extract just the main text, exclude child links
                                    main_text = ""
                                    for item in li.contents:
                                        if isinstance(item, str):
                                            main_text += item.strip()
                                        elif item.name == 'a' and 'jTips' in item.get('class', []):
                                            main_text += item.get_text(strip=True)
                                            href = item.get('href', '')
                                            if 'ItemID=' in href:
                                                item_id = href.split('ItemID=')[-1]
                                            else:
                                                item_id = info.get("document_id", "") if title_text == "Văn bản hiện thời" else ""
                                            
                                    if main_text:
                                        cleaned_text = re.sub(r'\s+', ' ', main_text).strip()
                                        append_data = {
                                            "title": cleaned_text,
                                            "id": item_id
                                        }
                                        relationship[title_text].append(append_data)

            info["relationship"] = relationship

        return info
    
    def get_document_content(self, id: str) -> dict:
        """
        Gets document content and info from VBPL.

        Args:
            id (str): Document ID to retrieve.

        Returns:
            dict: Dictionary containing document content and info.
                {
                    "html_content": str,
                    "soup": BeautifulSoup object,
                    "text_content": str,
                    "document_info": dict
                }
        """
        html_content = self.crawl_toanvan(id)
        if not html_content:
            return {}
            
        soup = self.parse_html(html_content)
        content = soup.find('div', class_='toanvancontent').get_text(strip=False) if soup.find('div', class_='toanvancontent') else ""
        if not content:
            return {}
            
        info = self.extract_info(soup)
        
        return {
            "html_content": html_content,
            "soup": soup,
            "text_content": content,
            "document_info": {
                "document_id": info.get("document_id", ""),
                "document_title": info.get("document_title", ""),
                "document_date": info.get("document_date", ""),
                "document_status": info.get("document_status", ""),
                "effective_date": info.get("effective_date", ""),
                "expired_date": info.get("expired_date", ""),
                "relationship": info.get("relationship", {})
            }
        }

    def _crawl_category_page(self, url: str) -> Tuple[List[Dict[str, Any]], Set[str]]:
        """Crawl a single category page and extract links and item IDs."""
        try:
            response = httpx.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links, item_ids = [], set()
            list_law = soup.find('ul', class_='listLaw')
            
            if list_law:
                for li in list_law.find_all('li'):
                    link = li.find('a', href=True)
                    if link and link.get('href', '').startswith('/nganhangnhanuoc/Pages/vbpq-toanvan.aspx'):
                        href = link['href']
                        item_match = re.search(r'ItemID=(\d+)', href)
                        item_id = item_match.group(1) if item_match else None
                        
                        if item_id:
                            item_ids.add(item_id)
                        
                        links.append({
                            'url': f"https://vbpl.vn{href}",
                            'text': link.get_text(strip=True),
                            'item_id': item_id
                        })
            
            return links, item_ids
            
        except Exception as e:
            logger.error(f"Error crawling page {url}: {e}")
            return [], set()

    def crawl_category(self, category: str, max_pages: int = None, save_to_file: bool = True) -> Tuple[List[Dict[str, Any]], Set[str]]:
        """
        Crawl documents by category from VBPL.
        
        Args:
            category: Category key (e.g., 'thong_tu', 'nghi_dinh')
            max_pages: Maximum number of pages to crawl (uses category default if None)
            save_to_file: Whether to save item IDs to JSON file
            
        Returns:
            Tuple of (all_links, item_ids)
        """
        if category not in self.categories:
            raise ValueError(f"unknown category: {category}. Available: {list(self.categories.keys())}")
        
        # Use category's default max_pages if not specified
        if max_pages is None:
            max_pages = self.categories[category]['max_pages']
        
        logger.info(f"Starting to crawl category: {self.categories[category]['name']} (max {max_pages} pages)")
        
        base_url = f"https://vbpl.vn/nganhangnhanuoc/Pages/vanban.aspx?idLoaiVanBan={self.categories[category]['idLoaiVanBan']}&dvid=326"
        all_links, all_ids = [], set()
        
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}&Page={page}"
            logger.debug(f"Crawling page {page}/{max_pages}")
            
            links, ids = self._crawl_category_page(page_url)
            all_links.extend(links)
            all_ids.update(ids)
            
            # Break if no links found on this page
            if not links:
                logger.info(f"No more links found at page {page}, stopping early")
                break
                
            time.sleep(1)  # Be respectful to the server
        
        logger.info(f"Crawling completed. Found {len(all_links)} links and {len(all_ids)} unique IDs")
        
        # Save results to file if requested
        if save_to_file:
            output_file = f"{category}_item_ids.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({"ItemID": list(all_ids)}, f, ensure_ascii=False, indent=2)
            logger.info(f"Item IDs saved to {output_file}")
        
        return all_links, all_ids

    def crawl_multiple_categories(self, categories: List[str], max_pages: int = None, save_to_file: bool = True) -> Dict[str, Tuple[List[Dict[str, Any]], Set[str]]]:
        """
        Crawl multiple document categories.
        
        Args:
            categories: List of category keys to crawl
            max_pages: Maximum number of pages to crawl per category (uses each category's default if None)
            save_to_file: Whether to save item IDs to JSON files
            
        Returns:
            Dictionary mapping category names to (all_links, item_ids) tuples
        """
        results = {}
        
        for category in categories:
            if category not in self.categories:
                logger.warning(f"Skipping unknown category: {category}")
                continue
                
            try:
                # Use category-specific max_pages if global max_pages is not provided
                category_max_pages = max_pages if max_pages is not None else self.categories[category]['max_pages']
                results[category] = self.crawl_category(category, category_max_pages, save_to_file)
                logger.info(f"Completed crawling {category}")
            except Exception as e:
                logger.error(f"Error crawling category {category}: {e}")
                continue
        
        return results
