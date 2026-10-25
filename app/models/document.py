from dataclasses import dataclass

@dataclass
class ExtractedDocument:
    file_path: str
    file_name: str
    extension: str
    page_start: int
    page_end: int
    text: str


from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connector import Base


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    extension: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    chunks = relationship(
        "DocumentChunkModel",
        back_populates="document",
        cascade="all, delete-orphan",
    )