from haystack_integrations.components.embedders.fastembed import (
    FastembedSparseDocumentEmbedder,
    FastembedSparseTextEmbedder,
)
from vietnam_law_chatbot.core.config import settings


def get_fastembed_sparse_document_embedder() -> FastembedSparseDocumentEmbedder:
    """
    Returns a FastembedSparseDocumentEmbedder instance.
    """
    model = settings.SPARSE_EMBEDDING_MODEL
    sparse_doc_embedder = FastembedSparseDocumentEmbedder(model=model)
    sparse_doc_embedder.warm_up()
    return sparse_doc_embedder


def get_fastembed_sparse_text_embedder() -> FastembedSparseTextEmbedder:
    """
    Returns a FastembedSparseTextEmbedder instance.
    """
    model = settings.SPARSE_EMBEDDING_MODEL
    sparse_text_embedder = FastembedSparseTextEmbedder(model=model)
    sparse_text_embedder.warm_up()
    return sparse_text_embedder