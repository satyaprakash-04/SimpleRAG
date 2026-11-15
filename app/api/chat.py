import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from database.connector import SessionLocal
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.repositories.vector_repository import VectorRepository
from app.services.chat_service import ChatService
from app.utils.sse import format_sse

router = APIRouter(prefix="/chat", tags=["Chat"])

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    session_id: UUID
    question: str = Field(
        min_length=1,
        max_length=10000,
    )


@router.post("/stream")
async def stream_chat(
    payload: ChatRequest,
    request: Request,
):
    db = SessionLocal()

    try:
        rag_service = request.app.state.rag_service

        conversation_repository = ConversationRepository(db)

        # Validate the session before starting the HTTP stream.
        conversation = (
            conversation_repository.get_by_session_id(
                payload.session_id
            )
        )

        if conversation is None:
            db.close()
            raise HTTPException(
                status_code=404,
                detail="Conversation session not found",
            )

        vector_repository = VectorRepository(db)

        chat_service = ChatService(
            conversation_repository=conversation_repository,
            vector_repository=vector_repository,
            rag_service=rag_service,
        )

    except HTTPException:
        raise
    except Exception:
        db.close()
        logger.exception("Failed to initialize chat request")
        raise HTTPException(
            status_code=500,
            detail="Could not initialize chat request",
        )

    async def event_generator():
        try:
            async for event in chat_service.stream_chat(
                session_id=payload.session_id,
                question=payload.question,
            ):
                yield format_sse(
                    event=event["type"],
                    data=event["data"],
                )

        except Exception:
            logger.exception(
                "Chat generation failed for session %s",
                payload.session_id,
            )

            yield format_sse(
                event="error",
                data={
                    "message": "An error occurred while generating the response.",
                },
            )

        finally:
            db.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
