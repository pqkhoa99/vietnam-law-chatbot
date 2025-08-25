from typing import Union

from haystack.components.embedders import (
    OpenAIDocumentEmbedder,
    OpenAITextEmbedder,
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)

from core.config import settings
from retrieval.embedders.openai import (
    get_openai_document_embedder,
    get_openai_text_embedder,
)
from retrieval.embedders.sentence_transformers import (
    get_sentence_transformers_document_embedder,
    get_sentence_transformers_text_embedder,
)


class EmbedderFactory:
    """
    A factory class for creating document and text embedders based on configuration.
    """

    @staticmethod
    def get_document_embedder() -> Union[OpenAIDocumentEmbedder, SentenceTransformersDocumentEmbedder]:
        """
        Returns a document embedder instance based on the EMBEDDER_TYPE in settings.
        """
        embedder_type = settings.EMBEDDER_TYPE

        if embedder_type == "openai":
            return get_openai_document_embedder()
        elif embedder_type == "sentence-transformers":
            return get_sentence_transformers_document_embedder()
        else:
            raise ValueError(f"unknown embedder type for documents: {embedder_type}")

    @staticmethod
    def get_text_embedder() -> Union[OpenAITextEmbedder, SentenceTransformersTextEmbedder]:
        """
        Returns a text embedder instance based on the EMBEDDER_TYPE in settings.
        This is useful for embedding single queries.
        """
        embedder_type = settings.EMBEDDER_TYPE

        if embedder_type == "openai":
            return get_openai_text_embedder()
        elif embedder_type == "sentence-transformers":
            return get_sentence_transformers_text_embedder()
        else:
            raise ValueError(f"unknown embedder type for text: {embedder_type}")


document_embedder = EmbedderFactory.get_document_embedder()
text_embedder = EmbedderFactory.get_text_embedder()