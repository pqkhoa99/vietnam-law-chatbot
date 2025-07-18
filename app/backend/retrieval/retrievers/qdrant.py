from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from backend.core.config import settings


def get_qdrant_retriever(
    document_store: QdrantDocumentStore,
) -> QdrantEmbeddingRetriever:
    """
    Returns a Qdrant embedding retriever instance.
    """
    return QdrantEmbeddingRetriever(document_store=document_store, top_k=settings.RETRIEVER_TOP_K)