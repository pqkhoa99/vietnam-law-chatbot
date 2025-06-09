"""
Configuration settings for the application.
"""
import os
from typing import List


from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    PROJECT_NAME: str = "Vietnam Legal Chatbot"
    PROJECT_DESCRIPTION: str = "API for the Vietnam Legal Chatbot RAG application"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_INDEX: str = "vietnam_legal_docs"
    
    # Neo4j settings
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # LLM settings
    DEFAULT_MODEL_NAME: str = "gpt-3.5-turbo"
    
    # Embedding settings
    EMBEDDER_TYPE: str = "openai"  # Options: "openai", "sentence-transformers"
    SPARSE_EMBEDDING_MODEL: str = "Qdrant/bm25"  # For sparse embeddings, e.g., BM25
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_BATCH_SIZE: int = 32
    EMBEDDING_DIMENSIONS: int = 384
    
    
    # Retrieval settings
    DOCUMENT_STORE_TYPE: str = "qdrant_hybrid"
    RETRIEVER_TOP_K: int = 5
    

    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"


# Create global settings instance
settings = Settings()
