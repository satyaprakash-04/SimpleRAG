from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connector import Base


@dataclass
class DocumentChunk:
    document_id: UUID
    chunk_index: int
    content: str
    file_path: str
    file_name: str
    page_start: int | None = None
    page_end: int | None = None
    metadata: dict = field(default_factory=dict)
    embedding: list[float] | None = None


EMBEDDING_DIMENSION = 384


class DocumentChunkModel(Base):

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    page_start: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    page_end: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    metadata_: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIMENSION),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    document = relationship(
        "Document",
        back_populates="chunks",
    )
