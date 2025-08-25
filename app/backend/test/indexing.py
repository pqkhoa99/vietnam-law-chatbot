import json
import sys
import os
import logging
from loguru import logger
from retrieval.indexing.crawler import VBPLCrawler
from retrieval.indexing.chunking import VBPLChunker
from core.config import settings
from core.utils import read_json_file, save_to_json_file
from retrieval.utils import insert
from haystack.dataclasses import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("crawl_chunk_test.log", rotation="10 MB")

# Sample document IDs to test
SAMPLE_DOCUMENT_IDS = [
    "176421",  # Example document ID
    # "167197",
    # "176696",
    # "177349",
    # "169527",
    # "178101",
    # Add more document IDs here for testing
]

# Ensure chunking directory exists
CHUNKING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chunking")
os.makedirs(CHUNKING_DIR, exist_ok=True)

def test_crawl_and_chunk_by_prefix(document_id):
    """
    Test crawling and chunking a document using prefix-based chunking.
    
    Args:
        document_id (str): The ID of the document to crawl and chunk.
    """
    logger.info(f"Testing crawl and chunk by prefix for document ID: {document_id}")
    
    # Initialize crawler
    crawler = VBPLCrawler()
    
    # Crawl the document
    document_data = crawler.get_document_content(document_id)
    
    if not document_data:
        logger.error(f"Failed to crawl document with ID: {document_id}")
        return
    
    logger.info(f"Successfully crawled document: {document_data.get('document_info', {}).get('document_title', 'unknown')}")
    
    # Initialize chunker
    from openai import OpenAI

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        max_retries=10,
    )

    chunker = VBPLChunker(openai_client=client)
    
    # Chunk the document by prefix
    chunked_data = chunker.chunking_by_prefix(document_data)
    
    if not chunked_data:
        logger.error(f"Failed to chunk document with ID: {document_id}")
        return
    
    # Save the chunked data to a file in the chunking directory
    output_filename = os.path.join(CHUNKING_DIR, f"{document_id}_prefix_chunking.json")
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(chunked_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Chunked data saved to {output_filename}")
    
    # Print statistics
    total_sections = len(chunked_data.get('data', []))
    total_articles = sum(1 for item in chunked_data.get('data', []) 
                         if item.get('type') == 'ARTICLE')
    total_articles += sum(len([c for c in item.get('children', []) if c.get('type') == 'ARTICLE']) 
                         for item in chunked_data.get('data', []))
    
    logger.info(f"Statistics for document {document_id}:")
    logger.info(f"Total top-level sections: {total_sections}")
    logger.info(f"Total articles: {total_articles}")


    # logger.info(chunker.chunking_articles(chunked_data))
    articles_data = chunker.chunking_articles(chunked_data)
    # Save the articles data to a file
    articles_output_filename = os.path.join(CHUNKING_DIR, f"{document_id}_articles.json")
    with open(articles_output_filename, "w", encoding="utf-8") as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    logger.info(f"Articles data saved to {articles_output_filename}")

def test_crawl_and_chunk_with_llm(document_id, openai_client=None):
    """
    Test crawling and chunking a document using LLM-based chunking.
    
    Args:
        document_id (str): The ID of the document to crawl and chunk.
        openai_client: OpenAI client for LLM-based chunking.
    """
    if not openai_client:
        logger.warning("OpenAI client not provided. Skipping LLM-based chunking.")
        return
    
    logger.info(f"Testing crawl and chunk with LLM for document ID: {document_id}")
    
    # Initialize crawler
    crawler = VBPLCrawler()
    
    # Crawl the document
    document_data = crawler.get_document_content(document_id)
    
    if not document_data:
        logger.error(f"Failed to crawl document with ID: {document_id}")
        return
    
    logger.info(f"Successfully crawled document: {document_data.get('document_info', {}).get('document_title', 'unknown')}")
    
    # Initialize chunker with OpenAI client
    chunker = VBPLChunker(openai_client=openai_client)
    
    # Chunk the document with LLM
    chunked_data = chunker.chunking_with_llm(document_data)
    
    if not chunked_data:
        logger.error(f"Failed to chunk document with LLM with ID: {document_id}")
        return
    
    # Save the chunked data to a file in the chunking directory
    output_filename = os.path.join(CHUNKING_DIR, f"{document_id}_llm_chunking.json")
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(chunked_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"LLM chunked data saved to {output_filename}")
    
    # Print statistics
    total_sections = len(chunked_data.get('data', []))
    total_articles = sum(1 for item in chunked_data.get('data', []) 
                         if item.get('type') == 'ARTICLE')
    total_articles += sum(len([c for c in item.get('children', []) if c.get('type') == 'ARTICLE']) 
                         for item in chunked_data.get('data', []))
    
    logger.info(f"LLM Statistics for document {document_id}:")
    logger.info(f"Total top-level sections: {total_sections}")
    logger.info(f"Total articles: {total_articles}")

def extract_dieu_data(dieu_id):
    """
    Extract article data from a specific document ID and save to JSON file.
    
    Args:
        dieu_id (str): The document ID to extract articles from
        
    Returns:
        list: List of extracted article data with id and content
    """    
    # Read the chunking data
    data = read_json_file('backend/data/chunking_data.json')
    dieu_info = []
    
    if dieu_id is None:
        for doc in data:
            dieu_info.extend(_extract_articles_from_parts(doc.get("data", [])))
            break
    else:
        for doc in data:
            if doc.get("document_info", {}).get("document_id") == dieu_id:
                dieu_info.extend(_extract_articles_from_parts(doc.get("data", [])))
                break
    
    # Save extracted data to file
    output_filename = f"backend/data/dieu_data_{dieu_id}.json"
    save_to_json_file(dieu_info, output_filename)
    return dieu_info

def _extract_articles_from_parts(parts):
    """
    Helper function to recursively extract articles from document parts.
    
    Args:
        parts (list): List of document parts (chapters, sections, articles)
        
    Returns:
        list: List of extracted articles with id and content
    """
    articles = []
    
    for part in parts:
        part_type = part.get("type")
        
        if part_type == "ARTICLE":
            # Direct article - extract it
            article_data = {
                "id": part.get("id"),
                "content": part.get("content", ""),
            }
            articles.append(article_data)
            
        elif part_type in ["CHAPTER", "SECTION"]:
            # Container element - recursively extract articles from children
            children = part.get("children", [])
            articles.extend(_extract_articles_from_parts(children))
            
        else:
            # unknown type - log warning
            logger.warning(f"unknown part type encountered: {part_type}")
    return articles

def embedding_dieu_data(dieu_id):
    """
    Embed article data from a specific document ID into Qdrant vector database.
    
    Args:
        dieu_id (str, optional): The document ID to embed articles from. 
                                If None, uses default dieu_data.json file.
        
    Returns:
        bool: True if embedding was successful, False otherwise
    """
    # Determine the data file path
    if dieu_id is None:
        data_file = 'backend/data/dieu_data.json'
    else:
        data_file = f'backend/data/dieu_data_{dieu_id}.json'
    
    dieu_data = read_json_file(data_file)
    documents = []

    for i, item in enumerate(dieu_data):            
        # Create Document object
        doc = Document(
            content=item['content'],
            meta={
                'id': item['id'],
            }
        )
        documents.append(doc)
        
    # Insert documents into Qdrant
    logger.info(f"📄 Embedding {len(documents)} documents into Qdrant...")
    insert(documents)
    logger.info("✅ Documents successfully embedded and stored in Qdrant!")


def extract_and_embed_dieu_data(dieu_id):
    """
    Complete pipeline to extract article data and embed it into Qdrant.
    
    Args:
        dieu_id (str): The document ID to extract and embed articles from
        
    Returns:
        bool: True if the complete pipeline was successful, False otherwise
    """
    try:
        # Step 1: Extract article data
        logger.info("📝 Step 1: Extracting article data...")
        articles = extract_dieu_data(dieu_id)
        # Step 2: Embed the extracted data
        logger.info("🔄 Step 2: Embedding article data...")
        embedding_dieu_data(dieu_id)
    except Exception as e:
        logger.error(f"❌ Pipeline failed for document ID {dieu_id}: {e}")
        return False

def main():
    """
    Main function to run the test.
    """

    embedding_dieu_data("160901")

    # logger.info("Starting crawl and chunk test")
    
    # # Process document IDs from command line if provided
    # document_ids = sys.argv[1:] if len(sys.argv) > 1 else SAMPLE_DOCUMENT_IDS
    
    # for document_id in document_ids:
    #     # Test prefix-based chunking
    #     test_crawl_and_chunk_by_prefix(document_id)
        
        # To test LLM-based chunking, uncomment and provide OpenAI client:
        # from openai import OpenAI
        # from core.config import settings

        # client = OpenAI(
        #     api_key=settings.OPENAI_API_KEY,
        #     base_url=settings.OPENAI_BASE_URL
        # )
        
        # test_crawl_and_chunk_with_llm(document_id, client)
    
    logger.info("Test completed")

if __name__ == "__main__":
    main()
