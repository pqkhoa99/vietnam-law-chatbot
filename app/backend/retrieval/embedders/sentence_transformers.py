from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)

from backend.core.config import settings


def get_sentence_transformers_document_embedder() -> SentenceTransformersDocumentEmbedder:
    """
    Returns a Sentence Transformers document embedder instance.
    """
    embedder = SentenceTransformersDocumentEmbedder(
        model=settings.EMBEDDING_MODEL_NAME,
        batch_size=settings.EMBEDDING_BATCH_SIZE,
    )
    embedder.warm_up()
    return embedder


def get_sentence_transformers_text_embedder() -> SentenceTransformersTextEmbedder:
    """
    Returns a Sentence Transformers text embedder instance.
    """
    embedder = SentenceTransformersTextEmbedder(
        model=settings.EMBEDDING_MODEL_NAME,
    )
    embedder.warm_up()
    return embedder