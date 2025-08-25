"""
Domain models for the Vietnam Law Chatbot API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class RelatedDocument(BaseModel):
    """Information about related documents through legal relationships."""

    rela_type: str = Field(..., description="Relationship type")
    id: str = Field(..., description="Document or article ID")
    title: str = Field("unknown", description="Title", alias="tittle")
    content: str = Field("unknown", description="Content")
    vbpl_id: str = Field("unknown", description="VBPL ID")
    document_id: str = Field("unknown", description="Document ID")
    document_title: str = Field("unknown", description="Document title", alias="document_tittle")
    document_status: str = Field("unknown", description="Status (e.g., Còn hiệu lực)")
    effective_date: str = Field("unknown", description="Effective date")
    expired_date: str = Field("unknown", description="Expiration date")


class Relationships(BaseModel):
    """Relationships object in retrieved documents."""

    incoming: List[RelatedDocument] = Field(default_factory=list, description="Incoming related articles")
    outgoing: List[RelatedDocument] = Field(default_factory=list, description="Outgoing related articles")


class RetrievedDocument(BaseModel):
    """Document retrieved from Qdrant vector search."""
    
    id: str = Field(..., description="Document or article ID")
    score: Optional[float] = Field(None, description="Relevance score from search")
    title: str = Field("unknown", description="Document title")
    content: str = Field("unknown", description="Document content")
    vbpl_id: str = Field("unknown", description="VBPL ID")
    document_id: str = Field("unknown", description="Document ID")
    document_title: str = Field("unknown", description="Full document title")
    document_status: str = Field("unknown", description="Status (e.g., Còn hiệu lực)")
    effective_date: str = Field("unknown", description="Effective date")
    expired_date: str = Field("unknown", description="Expiration date")
    sua_doi_bo_sung: Any = Field("unknown", description="Amendments")
    thay_the: Any = Field("unknown", description="Replacements")
    bai_bo: Any = Field("unknown", description="Abolitions")
    dinh_chi: Any = Field("unknown", description="Suspensions")
    huong_dan_quy_dinh: Any = Field("unknown", description="Guidance/Regulations")
    relationships: Relationships = Field(default_factory=Relationships, description="Incoming/outgoing relationships")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    message: str = Field(..., description="User's question or message", min_length=1, max_length=2000)
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Điều kiện để mở tài khoản ngân hàng là gì?",
                "session_id": "session_123",
                "context": {"user_type": "individual"}
            }
        }


class DocumentSource(BaseModel):
    """Information about a source document used in the response."""
    
    id: str = Field(..., description="Document or article ID")
    title: str = Field(..., description="Document or article title")
    document_id: str = Field(..., description="Official document identifier")
    document_title: str = Field(..., description="Official document title")
    document_status: str = Field(..., description="Document status (e.g., 'Còn hiệu lực')")
    effective_date: Optional[str] = Field(None, description="Document effective date")
    score: Optional[float] = Field(None, description="Relevance score from search")
    content_snippet: Optional[str] = Field(None, description="Relevant content snippet")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    message: str = Field(..., description="Generated response message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    related_documents: List[RetrievedDocument] = Field(default_factory=list, description="Related legal documents")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    services: Dict[str, str] = Field(..., description="Status of individual services")
    version: str = Field(..., description="API version")
