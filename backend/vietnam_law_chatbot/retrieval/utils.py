from typing import List
from haystack.dataclasses import Document
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

from vietnam_law_chatbot.core.config import settings
from vietnam_law_chatbot.retrieval.document_stores.factory import document_store
from vietnam_law_chatbot.retrieval.embedders.factory import document_embedder, text_embedder
from vietnam_law_chatbot.retrieval.retrievers.factory import retriever


def insert(documents: List[Document]):
    """
    Embeds and writes documents to the document store.
    Handles both dense and hybrid embedding strategies.
    """
    document_store_type = settings.DOCUMENT_STORE_TYPE
    writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.OVERWRITE)

    if document_store_type == "qdrant_hybrid":
        from vietnam_law_chatbot.retrieval.embedders.fastembed_sparse import get_fastembed_sparse_document_embedder

        sparse_doc_embedder = get_fastembed_sparse_document_embedder()

        # Embed documents with both sparse and dense embedders
        documents_with_sparse_embeddings = sparse_doc_embedder.run(documents=documents)["documents"]
        documents_with_all_embeddings = document_embedder.run(documents=documents_with_sparse_embeddings)["documents"]

        writer.run(documents=documents_with_all_embeddings)

    elif document_store_type == "qdrant":
        documents_with_embeddings = document_embedder.run(documents=documents)["documents"]
        writer.run(documents=documents_with_embeddings)
    else:
        raise ValueError(f"Unknown document store type for insertion: {document_store_type}")


def search(query: str) -> List[Document]:
    """
    Embeds a query and retrieves relevant documents from the document store.
    """
    document_store_type = settings.DOCUMENT_STORE_TYPE
    
    if document_store_type == "qdrant_hybrid":
        from vietnam_law_chatbot.retrieval.embedders.fastembed_sparse import get_fastembed_sparse_text_embedder

        sparse_text_embedder = get_fastembed_sparse_text_embedder()

        query_embedding = text_embedder.run(text=query)["embedding"]
        query_sparse_embedding = sparse_text_embedder.run(text=query)["sparse_embedding"]

        # The retriever is a QdrantHybridRetriever, which takes both embeddings
        results = retriever.run(
            query_embedding=query_embedding,
            query_sparse_embedding=query_sparse_embedding
        )
        return results["documents"]

    elif document_store_type == "qdrant":
        query_embedding = text_embedder.run(text=query)["embedding"]

        # The retriever is a QdrantEmbeddingRetriever
        results = retriever.run(query_embedding=query_embedding)
        return results["documents"]
    else:
        raise ValueError(f"Unknown document store type for searching: {document_store_type}")