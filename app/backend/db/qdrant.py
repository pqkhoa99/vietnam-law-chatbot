"""
Qdrant vector database client for the Vietnam Legal Chatbot.
"""
from typing import Dict, List, Optional, Union

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http.models import Distance, VectorParams

from core.config import settings


def get_qdrant_client() -> QdrantClient:
    """
    Get a Qdrant client instance.
    
    Returns:
        QdrantClient: Qdrant client
    """
    if settings.QDRANT_URL:
        client = QdrantClient(url=settings.QDRANT_URL)
    else:
        client = QdrantClient(path="./qdrant_data")
    
    return client


class QdrantManager:
    """Manager for Qdrant vector database operations."""
    
    def __init__(
        self,
        client: Optional[QdrantClient] = None,
        collection_name: str = settings.QDRANT_COLLECTION_NAME,
        vector_size: int = 384,  # Default for paraphrase-multilingual-MiniLM-L12-v2
    ):
        """
        Initialize the Qdrant manager.
        
        Args:
            client: Qdrant client
            collection_name: Name of the collection
            vector_size: Size of embedding vectors
        """
        self.client = client or get_qdrant_client()
        self.collection_name = collection_name
        self.vector_size = vector_size
        
        self._create_collection_if_not_exists()
    
    def _create_collection_if_not_exists(self) -> None:
        """Create the collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
    
    def add_documents(
        self,
        documents: List[Dict[str, str]],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector database.
        
        Args:
            documents: Document dictionaries with metadata
            embeddings: Embedding vectors
            ids: Optional document IDs
            
        Returns:
            List of document IDs
        """
        if ids is None:
            ids = [str(i) for i in range(len(documents))]
            
        points = [
            rest.PointStruct(
                id=id_,
                vector=embedding,
                payload=document
            )
            for id_, embedding, document in zip(ids, embeddings, documents)
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return ids
    
    def search_similar(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = 0.7
    ) -> List[Dict]:
        """
        Search for similar documents.
        
        Args:
            query_vector: Query embedding
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            
        Returns:
            List of documents with similarity scores
        """
        search_params = {}
        if score_threshold is not None:
            search_params["score_threshold"] = score_threshold
            
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            search_params=search_params
        )
        
        return [
            {**result.payload, "score": result.score} 
            for result in results
        ]
