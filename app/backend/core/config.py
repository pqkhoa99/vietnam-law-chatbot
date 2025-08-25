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
    DEBUG_MODE: bool = True
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:8000"]

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_INDEX: str = "vietnam_law_docs"
    
    # Neo4j settings
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"
        
    # Embedding settings
    EMBEDDER_TYPE: str = "openai"
    SPARSE_EMBEDDING_MODEL: str = "Qdrant/bm25"
    EMBEDDING_MODEL_NAME: str = "gpt-5-mini"
    EMBEDDING_BATCH_SIZE: int = 32
    EMBEDDING_DIMENSIONS: int = 1536
    
    # Retrieval settings
    DOCUMENT_STORE_TYPE: str = "qdrant_hybrid"
    RETRIEVER_TOP_K: int = 5
    RETRIEVER_SCORE_THRESHOLD: float = 0.7
    
    # OpenAI settings
    DEFAULT_MODEL_NAME: str = "gpt-5-mini"
    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-5-mini"
    OPENAI_PARSE_MODEL: str = "gpt-5-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Generation settings
    MAX_INPUT_TOKENS: int = 250000
    GENERATION_TEMPERATURE: float = 0.1
    GENERATION_MAX_TOKENS: int = 50000
    GENERATION_TOP_P: float = 1.0

    # Parse settings
    CONCURRENCY_LIMIT: int = 5

# Create global settings instance
settings = Settings()
