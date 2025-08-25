from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from core.config import settings


def get_qdrant_document_store() -> QdrantDocumentStore:
    """
    Returns a Qdrant document store instance.
    """
    return QdrantDocumentStore(
        url=settings.QDRANT_URL,
        index=settings.QDRANT_INDEX,
        embedding_dim=settings.EMBEDDING_DIMENSIONS,
        recreate_index=False,
        hnsw_config={"m": 16, "ef_construct": 64},
        use_sparse_embeddings=False,
    )