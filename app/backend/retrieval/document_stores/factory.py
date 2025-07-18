from haystack.document_stores.types import DocumentStore
from backend.core.config import settings
from backend.retrieval.document_stores.qdrant import get_qdrant_document_store
from backend.retrieval.document_stores.qdrant_hybrid import (
    get_qdrant_hybrid_document_store,
)


class DocumentStoreFactory:
    """
    A factory class for creating document stores based on configuration.
    """

    @staticmethod
    def get_document_store() -> DocumentStore:
        """
        Returns a document store instance based on the DOCUMENT_STORE_TYPE in settings.
        """
        document_store_type = settings.DOCUMENT_STORE_TYPE

        if document_store_type == "qdrant":
            return get_qdrant_document_store()
        elif document_store_type == "qdrant_hybrid":
            return get_qdrant_hybrid_document_store()
        else:
            raise ValueError(f"Unknown document store type: {document_store_type}")


document_store = DocumentStoreFactory.get_document_store()