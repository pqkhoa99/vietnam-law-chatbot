"""
OpenAI-based text generation component for RAG.
"""
from typing import List, Optional, Dict, Any
import openai
from haystack.dataclasses import Document
from backend.core.config import settings
from backend.core.prompts import VIETNAMESE_LEGAL_ASSISTANT_PROMPT, RAG_CONTEXT_INSTRUCTION


class OpenAIGenerator:
    """
    OpenAI-based text generator for RAG applications.
    """
    
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        base_url: str = None,
        temperature: float = 0.1,
        max_tokens: int = 1000,
        top_p: float = 1.0
    ):
        """
        Initialize the OpenAI generator.
        
        Args:
            model: OpenAI model name
            api_key: OpenAI API key
            base_url: OpenAI base URL
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Top-p sampling parameter
        """
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=api_key or settings.OPENAI_API_KEY,
            base_url=base_url or settings.OPENAI_BASE_URL
        )
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None
    ) -> str:
        """
        Generate a response using OpenAI's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            top_p: Override default top_p
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                top_p=top_p or self.top_p
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            raise e
    
    def generate_rag_response(
        self,
        query: str,
        context_documents: List[Document],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a RAG response given a query and context documents.
        
        Args:
            query: User query
            context_documents: Retrieved documents for context
            system_prompt: Custom system prompt
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            
        Returns:
            Generated response
        """
        # Format context from documents
        context = self._format_context(context_documents)
        
        # Use default Vietnamese legal system prompt if none provided
        if system_prompt is None:
            system_prompt = VIETNAMESE_LEGAL_ASSISTANT_PROMPT
        
        # Create messages with context instruction
        context_with_instruction = f"{RAG_CONTEXT_INSTRUCTION}\n\n{context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context_with_instruction}\n\nCâu hỏi: {query}"}
        ]
        
        return self.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def _format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "Không có thông tin liên quan được tìm thấy."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            # Extract metadata if available
            metadata = ""
            if hasattr(doc, 'meta') and doc.meta:
                # Add document source information
                if 'source' in doc.meta:
                    metadata += f"Nguồn: {doc.meta['source']}\n"
                if 'title' in doc.meta:
                    metadata += f"Tiêu đề: {doc.meta['title']}\n"
                if 'article_id' in doc.meta:
                    metadata += f"Điều: {doc.meta['article_id']}\n"
            
            context_parts.append(f"Tài liệu {i}:\n{metadata}{doc.content}\n")
        
        return "\n".join(context_parts)


def get_openai_generator(**kwargs) -> OpenAIGenerator:
    """
    Factory function to create OpenAI generator instance.
    
    Args:
        **kwargs: Additional arguments for OpenAIGenerator
        
    Returns:
        OpenAI generator instance
    """
    return OpenAIGenerator(**kwargs)
