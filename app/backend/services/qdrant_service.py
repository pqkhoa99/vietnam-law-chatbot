from typing import List, Dict, Any, Literal
from qdrant_client import QdrantClient
import logging

from domain.models import RetrievedDocument
from core.config import settings
from retrieval.utils import search

logger = logging.getLogger(__name__)
RetrievalMode = Literal["dense", "sparse", "hybrid"]

class QdrantService:
    """Service for Qdrant vector database operations."""
    
    def __init__(self):
        self.config = settings
        self.client = QdrantClient(url=settings.QDRANT_URL)
    
    async def embed_query(self, query: str) -> List[float]:
        """Generate embeddings for a query text."""
        try:
            embedding = await self.adapter.embed_text(query)
            logger.info(f"Generated embedding for query: {query[:50]}...")
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to embed query: {e}")
            raise
    
    async def retrieve_similar_documents(
            self, 
            query: str, 
            mode: RetrievalMode = "hybrid",
            top_k: int = 5,
            threshold: float = 0.5
        ) -> List[RetrievedDocument]:
            """Retrieve documents similar to the query using specified mode."""
            
            try:                
                # Use existing search function from retrieval utils
                search_results = search(query)
                
                # Convert to domain models
                retrieved_docs = []
                for doc in search_results:
                    # Extract metadata following the specified format
                    retrieved_doc = RetrievedDocument(
                        id=doc.meta.get("id", "unknown"),
                        score=getattr(doc, "score", None),
                        title=doc.meta.get("title", "unknown"),
                        content=getattr(doc, "content", None),
                        vbpl_id=doc.meta.get("vbpl_id", "unknown"),
                        document_id=doc.meta.get("document_id", "unknown"),
                        document_title=doc.meta.get("document_title", "unknown"),
                        document_status=doc.meta.get("document_status", "unknown"),
                        effective_date=doc.meta.get("effective_date", "unknown"),
                        expired_date=doc.meta.get("expired_date", "unknown"),
                        sua_doi_bo_sung=doc.meta.get("sua_doi_bo_sung", "unknown"),
                        thay_the=doc.meta.get("thay_the", "unknown"),
                        bai_bo=doc.meta.get("bai_bo", "unknown"),
                        dinh_chi=doc.meta.get("dinh_chi", "unknown"),
                        huong_dan_quy_dinh=doc.meta.get("huong_dan_quy_dinh", "unknown"),
                    )        
                    retrieved_docs.append(retrieved_doc)
                logger.info(f"Sucessfully retrieved {len(retrieved_docs)} documents [document IDs: {[doc.id for doc in retrieved_docs]}]")

                # Apply threshold filtering
                filtered_docs = [doc for doc in retrieved_docs if doc.score >= threshold]
                logger.info(f"Filtered down to {len(filtered_docs)} documents above threshold {threshold} [document IDs: {[doc.id for doc in filtered_docs]}]")

                return filtered_docs

            except Exception as e:
                logger.error(f"Failed to retrieve similar documents: {e}")
                raise
        
    async def health_check(self) -> bool:
        """Check if Qdrant is healthy."""
        try:
            if not self.client:
                logger.error("Qdrant client not initialized")
                return False
                
            # Test connection
            collections = self.client.get_collections()
            logger.info(f"Qdrant connected. Available collections: {[col.name for col in collections.collections]}")
            
            # Check if our specific collection exists and get document count
            try:
                collection_info = self.client.get_collection(settings.qdrant_index)
                doc_count = collection_info.points_count
                logger.info(f"Collection '{settings.qdrant_index}' contains {doc_count} documents")
            except Exception as e:
                logger.warning(f"Collection '{settings.qdrant_index}' not found or empty: {e}")
                doc_count = 0
            
            return True
            
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False


# Global service instance
qdrant_service = QdrantService()
