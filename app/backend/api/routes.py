from fastapi import APIRouter, HTTPException
from loguru import logger

from backend.domain.models import ChatRequest, ChatResponse, HealthResponse
from backend.services.chat_service import ChatService
from backend.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message through linear RAG flow: Qdrant → Neo4j → LLM.
    """
    try:
        logger.info(f"Processing chat request: {request.message[:100]}...")
        
        # Validate message length
        if len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Process through linear flow
        response = await chat_service.process_chat(request)
        
        logger.info(f"Chat response generated successfully in {response.metadata.get('processing_time', 0):.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing your request"
        )


@router.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint to verify service status.
    """
    try:
        # Get health status from chat service
        services_status = await chat_service.health_check()
        
        # Determine overall status
        overall_status = "healthy"
        for service, status in services_status.items():
            if status != "healthy":
                overall_status = "degraded"
                break
        
        return HealthResponse(
            status=overall_status,
            services=services_status,
            version=settings.VERSION
        )
        
    except Exception as e:
        logger.error(f"Health check endpoint error: {e}")
        return HealthResponse(
            status="unhealthy",
            services={"error": str(e)},
            version=settings.VERSION
        )
