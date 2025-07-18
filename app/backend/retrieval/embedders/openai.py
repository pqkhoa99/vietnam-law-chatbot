from haystack.components.embedders import (
    OpenAIDocumentEmbedder,
    OpenAITextEmbedder,
)
from haystack.utils import Secret

from backend.core.config import settings


def get_openai_document_embedder() -> OpenAIDocumentEmbedder:
    """
    Returns an OpenAI document embedder instance.
    """
    return OpenAIDocumentEmbedder(
        api_key=Secret.from_token(settings.OPENAI_API_KEY),
        api_base_url=settings.OPENAI_BASE_URL,
        model=settings.OPENAI_EMBEDDING_MODEL,
        batch_size=settings.EMBEDDING_BATCH_SIZE,
        dimensions=settings.EMBEDDING_DIMENSIONS,
    )


def get_openai_text_embedder() -> OpenAITextEmbedder:
    """
    Returns an OpenAI text embedder instance.
    """
    return OpenAITextEmbedder(
        api_key=Secret.from_token(settings.OPENAI_API_KEY),
        api_base_url=settings.OPENAI_BASE_URL,
        model=settings.OPENAI_EMBEDDING_MODEL,
        dimensions=settings.EMBEDDING_DIMENSIONS,
    )