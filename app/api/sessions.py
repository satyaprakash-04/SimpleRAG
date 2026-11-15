from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database.connector import SessionLocal
from app.repositories.conversation_repository import (
    ConversationRepository,
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_session(db: Session = Depends(get_db)):

    repository = ConversationRepository(db)

    conversation = repository.create_session()

    return {
        "session_id": str(conversation.session_id),
        "message": "Conversation created successfully",
    }

@router.get("/{session_id}/messages")
def get_messages(
    session_id: UUID,
    db: Session = Depends(get_db),
):

    repository = ConversationRepository(db)

    try:
        conversation = repository.get_or_create(session_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = repository.get_conversation_messages(
        conversation.id
    )

    return {
        "session_id": str(session_id),
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }