"""
Synthesis service for LLM-based response generation.
"""
from typing import List
import json
import tiktoken
from openai import OpenAI
from loguru import logger
import logging

from core.config import settings
from core.prompts import LEGAL_RAG_PROMPT
from domain.models import RetrievedDocument

logger = logging.getLogger(__name__)

class SynthesisService:
    """Service for synthesizing responses using LLM."""
    
    def __init__(self):
        """Initialize synthesis service."""

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        logger.info("SynthesisService initialized")
    
    def generate_response(
        self, 
        query: str, 
        related_documents: List[RetrievedDocument],
    ) -> str:
        """
        Generate response using retrieved documents and relationships.
        """
        try:
            context = self._prepare_structured_context(related_documents)

            content = f"""
                <input>{query}</input>
                <legal_documents>{context}</legal_documents>
            """.strip()

            logger.info(f"Prepared context for query ~{self._count_tokens(context)}")
                
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": LEGAL_RAG_PROMPT},
                    {"role": "user", "content": content}
                ],
                temperature=settings.GENERATION_TEMPERATURE,
            )
            
            generated_response = response.choices[0].message.content
            logger.info(f"Successfully generated response using OpenAI model {settings.OPENAI_MODEL}")
            
            return generated_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi tạo phản hồi. Vui lòng thử lại sau."
    
    def _prepare_structured_context(self, retrieved_documents: List[RetrievedDocument]) -> str:
        """
        Prepare structured context with relationship information from retrieved documents.
        """
        documents_data = []
        
        for doc in retrieved_documents:
            # Prepare main document info
            doc_data = {
                "id": doc.id,
                "title": doc.title,
                "vbpl_id": doc.vbpl_id,
                "document_id": doc.document_id,
                "document_title": doc.document_title,
                "document_status": doc.document_status,
                "effective_date": doc.effective_date,
                "expired_date": doc.expired_date,
                "content": doc.content
            }
            
            # Add relationship information
            relationships = {}
            
            # Process relationship fields from chunking
            if hasattr(doc, 'sua_doi_bo_sung') and doc.sua_doi_bo_sung != "unknown":
                relationships["Sửa đổi, bổ sung"] = doc.sua_doi_bo_sung
                
            if hasattr(doc, 'thay_the') and doc.thay_the != "unknown":
                relationships["Thay thế"] = doc.thay_the
                
            if hasattr(doc, 'bai_bo') and doc.bai_bo != "unknown":
                relationships["Bãi bỏ"] = doc.bai_bo
                
            if hasattr(doc, 'dinh_chi') and doc.dinh_chi != "unknown":
                relationships["Đình chỉ việc thi hành"] = doc.dinh_chi
                
            if hasattr(doc, 'huong_dan_quy_dinh') and doc.huong_dan_quy_dinh != "unknown":
                relationships["Hướng dẫn, quy định"] = doc.huong_dan_quy_dinh
            
            # Process incoming and outgoing relationships
            if doc.relationships:
                if doc.relationships.incoming:
                    relationships["incoming_references"] = [
                        {
                            "relationship_type": rel.rela_type,
                            "id": rel.id,
                            "title": rel.title,
                            "document_id": rel.document_id,
                            "document_title": rel.document_title,
                            "document_status": rel.document_status,
                            "effective_date": rel.effective_date,
                            "expired_date": rel.expired_date,
                            "content_snippet": rel.content[:200] + "..." if len(rel.content) > 200 else rel.content
                        } for rel in doc.relationships.incoming
                    ]
                
                if doc.relationships.outgoing:
                    relationships["outgoing_references"] = [
                        {
                            "relationship_type": rel.rela_type,
                            "id": rel.id,
                            "title": rel.title,
                            "document_id": rel.document_id,
                            "document_title": rel.document_title,
                            "document_status": rel.document_status,
                            "effective_date": rel.effective_date,
                            "expired_date": rel.expired_date,
                            "content_snippet": rel.content[:200] + "..." if len(rel.content) > 200 else rel.content
                        } for rel in doc.relationships.outgoing
                    ]
            
            if relationships:
                doc_data["relationships"] = relationships
            
            documents_data.append(doc_data)
        
        # Convert to JSON for structured representation
        return json.dumps(documents_data, ensure_ascii=False, indent=2)
    
    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken.
        """
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            logger.warning(f"Token counting failed, using character estimate: {e}")
            return len(text) // 4  # Rough estimate: 4 chars per token
    
    
    def health_check(self) -> bool:
        """
        Check if the synthesis service is healthy.
        """
        try:
            # Test a simple API call to verify OpenAI connection
            test_response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=settings.GENERATION_MAX_TOKENS
            )
            return test_response.choices[0].message.content is not None
        except Exception as e:
            logger.error(f"Synthesis service health check failed: {str(e)}")
            return False


# Global service instances
synthesis_service = SynthesisService()
