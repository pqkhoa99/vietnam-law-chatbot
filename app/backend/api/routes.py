"""
API routes for the Vietnam Legal Chatbot.
"""
from fastapi import APIRouter

# Use absolute imports instead of relative imports
from api.v1.endpoints import chat, health

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
