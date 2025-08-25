import time
import uuid
from datetime import datetime
import logging

from domain.models import ChatRequest, ChatResponse
from services.qdrant_service import qdrant_service, RetrievalMode
from services.neo4j_service import neo4j_service
from services.synthesis_service import synthesis_service
from core.config import settings

logger = logging.getLogger(__name__)


class ChatService:
    """Main chat service."""
    
    def __init__(self):
        self.qdrant_service = qdrant_service
        self.neo4j_service = neo4j_service
        self.synthesis_service = synthesis_service
    
    async def process_chat(
        self, 
        request: ChatRequest, 
        retrieval_mode: RetrievalMode = "hybrid"
    ) -> ChatResponse:
        """Process chat request through the linear flow pipeline."""
        start_time = time.time()
        
        try:
            # Generate conversation ID if not provided
            session_id = request.session_id or f"conv_{uuid.uuid4().hex[:8]}"
            
            logger.info(f"Processing chat request (ID: {session_id} )")
            
            # Step 1: Qdrant retrieval
            logger.info(f"Step 1: Retrieving similar documents from Qdrant using {retrieval_mode} mode")
            retrieved_documents = await self.qdrant_service.retrieve_similar_documents(
                query=request.message,
                mode=retrieval_mode,
                top_k=settings.RETRIEVER_TOP_K,
                threshold=settings.RETRIEVER_SCORE_THRESHOLD
            )
            
            # Step 2: Neo4j expansion
            logger.info("Step 2: Expanding with related documents and relationships from Neo4j")
            related_documents = self.neo4j_service.get_document_relationships(
                query=request.message,
                documents=retrieved_documents
            )
            
            # Step 3: LLM synthesis
            logger.info("Step 3: Synthesizing response using LLM")
            response_text = self.synthesis_service.generate_response(
                query=request.message,
                related_documents=related_documents
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
        
            # Create response
            chat_response = ChatResponse(
                message=response_text,
                session_id=session_id,
                related_documents=related_documents,
                timestamp=datetime.now(),
                metadata={"processing_time": processing_time}
            )
            
            logger.info(f"Response for request (ID: {session_id}): {chat_response.message}...")
            return chat_response
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Failed to process chat request (ID: {session_id}): {e}")
            # Return error response
            processing_time = time.time() - start_time
            return ChatResponse(
                message=f"Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn: {str(e)}",
                session_id=request.session_id or f"conv_{uuid.uuid4().hex[:8]}",
                related_documents=[],
                timestamp=datetime.now(),
                metadata={"processing_time": processing_time}
            )
    
    async def health_check(self) -> dict:
        """Check health of all services."""
        try:
            logger.info("🔍 Starting comprehensive health check...")
            
            # Check Qdrant
            logger.info("🔍 Checking Qdrant vector database...")
            qdrant_healthy = await self.qdrant_service.health_check()
            
            # Check Neo4j
            logger.info("🔍  Checking Neo4j graph database...")
            neo4j_healthy = await self.neo4j_service.health_check()
            
            # Check LLM
            logger.info("🔍 Checking LLM service...")
            llm_healthy = self.synthesis_service.health_check()
            
            services_status = {
                "qdrant": "connected" if qdrant_healthy else "disconnected",
                "neo4j": "connected" if neo4j_healthy else "disconnected", 
                "llm": "available" if llm_healthy else "unavailable"
            }
            
            overall_status = "healthy" if all([qdrant_healthy, neo4j_healthy, llm_healthy]) else "unhealthy"
            
            if overall_status == "healthy":
                logger.info("✅ All services are healthy!")
            else:
                logger.warning("⚠️  Some services are experiencing issues")
            
            return {
                "status": overall_status,
                "services": services_status,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return {
                "status": "error",
                "services": {
                    "qdrant": "unknown",
                    "neo4j": "unknown",
                    "llm": "unknown"
                },
                "timestamp": datetime.now(),
                "error": str(e)
            }


# Global service instance
chat_service = ChatService()
