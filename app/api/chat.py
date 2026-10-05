from fastapi import APIRouter

from app.models.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

chat_service = ChatService()


@router.post("/",response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await chat_service.generate_response(request.message)

    return ChatResponse(response=response)