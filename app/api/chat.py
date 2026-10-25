from collections.abc import AsyncIterator
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connector import SessionLocal
from app.repositories.vector_repository import VectorRepository
from app.services.rag_service import RAGService
from app.clients.sentense_transformer_client import (
    SentenceTransformerClient,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # In production, share these heavyweight clients through
    # application lifespan/dependency injection rather than
    # constructing a model for every request.
    embedding_client = SentenceTransformerClient(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_repository = VectorRepository(db)

    rag_service = RAGService(
        embedding_client=embedding_client,
        vector_repository=vector_repository,
        model_name="gemma4:e2b",
        num_ctx=4096,
        top_k=5,
    )

    return rag_service.ask(request.question)

@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    # Use your application's shared, initialized RAG service.
    embedding_client = SentenceTransformerClient(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_repository = VectorRepository(db)

    rag_service = RAGService(
        embedding_client=embedding_client,
        vector_repository=vector_repository,
        model_name="gemma4:e2b",
        num_ctx=4096,
        top_k=5,
    )

    async def generate() -> AsyncIterator[str]:
        async for token in rag_service.stream_answer(
            request.question
        ):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )