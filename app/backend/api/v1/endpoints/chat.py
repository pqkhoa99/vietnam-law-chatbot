"""
Chat endpoints for the legal chatbot.
"""
from fastapi import APIRouter, Depends, HTTPException

from models.schemas import ChatRequest, ChatResponse


class ChatService:
    def generate_response(self, query, chat_history):
        return ChatResponse(
            answer="This is a placeholder response. Service not yet implemented.",
            sources=[],
            chat_history=chat_history + [{"role": "assistant", "content": "Placeholder response"}],
        )


router = APIRouter()


@router.post("", response_model=ChatResponse)
async def generate_response(
    request: ChatRequest,
    chat_service: ChatService = Depends(),
):
    """
    Generate a response to a user query.
    """
    try:
        response = chat_service.generate_response(
            query=request.query,
            chat_history=request.chat_history,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
