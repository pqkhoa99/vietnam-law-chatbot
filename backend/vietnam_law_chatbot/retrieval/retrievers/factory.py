from vietnam_law_chatbot.core.config import settings
from vietnam_law_chatbot.retrieval.document_stores import document_store
from vietnam_law_chatbot.retrieval.retrievers.qdrant import get_qdrant_retriever
from vietnam_law_chatbot.retrieval.retrievers.qdrant_hybrid import (
    get_qdrant_hybrid_retriever,
)
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever, QdrantHybridRetriever
from typing import Union

class RetrieverFactory:
    """
    A factory class for creating document retrievers based on configuration.
    """

    @staticmethod
    def get_retriever() -> Union[QdrantEmbeddingRetriever, QdrantHybridRetriever]:
        """
        Returns a document retriever instance based on the DOCUMENT_STORE_TYPE in settings.
        """
        document_store_type = settings.DOCUMENT_STORE_TYPE
        
        if document_store_type == "qdrant":
            return get_qdrant_retriever(document_store)
        elif document_store_type == "qdrant_hybrid":
            return get_qdrant_hybrid_retriever(document_store)
        else:
            raise ValueError(
                f"Unknown document store type for retriever: {document_store_type}"
            )


retriever = RetrieverFactory.get_retriever()