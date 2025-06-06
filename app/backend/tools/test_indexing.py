import json
import sys
import os
import logging
from loguru import logger
from tools.crawl import VBPLCrawler
from tools.chunking import VBPLChunker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("crawl_chunk_test.log", rotation="10 MB")

# Sample document IDs to test
SAMPLE_DOCUMENT_IDS = [
    "176421",  # Example document ID
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
    
    logger.info(f"Successfully crawled document: {document_data.get('document_info', {}).get('document_title', 'Unknown')}")
    
    # Initialize chunker
    chunker = VBPLChunker()
    
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
    
    logger.info(f"Successfully crawled document: {document_data.get('document_info', {}).get('document_title', 'Unknown')}")
    
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

def main():
    """
    Main function to run the test.
    """
    logger.info("Starting crawl and chunk test")
    
    # Process document IDs from command line if provided
    document_ids = sys.argv[1:] if len(sys.argv) > 1 else SAMPLE_DOCUMENT_IDS
    
    for document_id in document_ids:
        # Test prefix-based chunking
        test_crawl_and_chunk_by_prefix(document_id)
        
        # To test LLM-based chunking, uncomment and provide OpenAI client:
        # 
        # from openai import OpenAI
        # client = OpenAI(api_key="your-api-key")
        # test_crawl_and_chunk_with_llm(document_id, client)
    
    logger.info("Test completed")

if __name__ == "__main__":
    main()
