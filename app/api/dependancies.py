
from fastapi import Request
from sqlalchemy.orm import Session

from database.connector import SessionLocal
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.repositories.vector_repository import (
    VectorRepository,
)
from app.services.chat_service import ChatService


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_rag_service(request: Request):
    return request.app.state.rag_service


def get_chat_service(
    db: Session,
    rag_service,
) -> ChatService:
    conversation_repository = ConversationRepository(db)
    vector_repository = VectorRepository(db)

    return ChatService(
        conversation_repository=conversation_repository,
        vector_repository=vector_repository,
        rag_service=rag_service,
    )
