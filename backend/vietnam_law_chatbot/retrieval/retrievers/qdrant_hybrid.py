from haystack_integrations.components.retrievers.qdrant import QdrantHybridRetriever
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from vietnam_law_chatbot.core.config import settings


def get_qdrant_hybrid_retriever(
    document_store: QdrantDocumentStore,
) -> QdrantHybridRetriever:
    """
    Returns a Qdrant hybrid retriever instance.
    """
    return QdrantHybridRetriever(document_store=document_store, top_k=settings.RETRIEVER_TOP_K)