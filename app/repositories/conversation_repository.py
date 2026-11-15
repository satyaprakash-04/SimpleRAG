
from uuid import UUID

from sqlalchemy import select

from app.models.conversation import ConversationModel
from app.models.messages import MessageModel


class ConversationRepository:
    def __init__(self, db):
        self.db = db

    def get_by_session_id(
        self,
        session_id: UUID,
    ):
        statement = select(ConversationModel).where(
            ConversationModel.session_id == session_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def add_message(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
    ):
        message = MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)

        # Also update the conversation timestamp.
        conversation = self.db.get(
            ConversationModel,
            conversation_id,
        )

        if conversation is not None:
            from datetime import datetime, timezone
            conversation.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(message)

        return message

    def get_recent_messages(
        self,
        conversation_id: UUID,
        limit: int = 10,
    ):
        statement = (
            select(MessageModel)
            .where(
                MessageModel.conversation_id == conversation_id
            )
            .order_by(
                MessageModel.created_at.desc(),
                MessageModel.id.desc(),
            )
            .limit(limit)
        )

        messages = list(
            self.db.execute(statement).scalars().all()
        )

        # Return chronological order for the LLM.
        return list(reversed(messages))
