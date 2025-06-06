"""
Pydantic schemas for the API.
"""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str
    message: Optional[str] = None
    version: Optional[str] = None


class ChatMessage(BaseModel):
    """Chat message schema."""
    
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Chat request schema."""
    
    query: str = Field(..., description="User's question or query")
    chat_history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        description="Previous messages in the conversation",
    )


class Source(BaseModel):
    """Source document schema."""
    
    document_id: str
    document_name: str
    relevance_score: float
    content_preview: str


class ChatResponse(BaseModel):
    """Chat response schema."""
    
    answer: str
    sources: List[Source] = Field(default_factory=list)
    chat_history: List[ChatMessage]


class DocumentResponse(BaseModel):
    """Document processing response schema."""
    
    message: str
    document_id: str
    chunks_created: int
