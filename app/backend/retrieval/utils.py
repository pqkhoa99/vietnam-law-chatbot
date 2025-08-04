from typing import List, Optional
from haystack.dataclasses import Document
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

from backend.core.config import settings
from backend.retrieval.document_stores.factory import document_store
from backend.retrieval.embedders.factory import document_embedder, text_embedder
from backend.retrieval.retrievers.factory import retriever
from backend.retrieval.generation.factory import generator


def insert(documents: List[Document]):
    """
    Embeds and writes documents to the document store.
    Handles both dense and hybrid embedding strategies.
    """
    document_store_type = settings.DOCUMENT_STORE_TYPE
    writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.OVERWRITE)

    if document_store_type == "qdrant_hybrid":
        from backend.retrieval.embedders.fastembed_sparse import get_fastembed_sparse_document_embedder

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
        from backend.retrieval.embedders.fastembed_sparse import get_fastembed_sparse_text_embedder

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


def generate_response(
    query: str,
    context_documents: Optional[List[Document]] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 1000
) -> str:
    """
    Generate a response using RAG (Retrieval-Augmented Generation).
    """
    if context_documents is None:
        context_documents = search(query)
    
    # Generate response using the retrieved context
    response = generator.generate_rag_response(
        query=query,
        context_documents=context_documents,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response


def ask_question(query: str, **kwargs) -> dict:
    """
    Complete RAG pipeline: retrieve relevant documents and generate response.
    """
    try:
        # Retrieve relevant documents
        context_documents = search(query)
        
        # Generate response
        response = generate_response(
            query=query,
            context_documents=context_documents,
            **kwargs
        )
        
        # Extract metadata from documents
        metadata = {
            "num_retrieved_docs": len(context_documents),
            "document_sources": []
        }
        
        for doc in context_documents:
            if hasattr(doc, 'meta') and doc.meta:
                doc_meta = {
                    "score": getattr(doc, 'score', None),
                    "source": doc.meta.get('source', 'Unknown'),
                    "title": doc.meta.get('title', 'Unknown'),
                    "article_id": doc.meta.get('article_id', 'Unknown')
                }
                metadata["document_sources"].append(doc_meta)
        
        return {
            "query": query,
            "response": response,
            "context_documents": context_documents,
            "metadata": metadata
        }
        
    except Exception as e:
        print(f"Error in ask_question: {e}")
        return {
            "query": query,
            "response": f"Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn: {str(e)}",
            "context_documents": [],
            "metadata": {"error": str(e)}
        }