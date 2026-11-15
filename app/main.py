
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.sentense_transformer_client import (
    SentenceTransformerClient,
)
from app.services.rag_service import RAGService


@asynccontextmanager
async def lifespan(rag_app: FastAPI):
    # Load the embedding model only once.
    embedding_client = SentenceTransformerClient(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Initialize the shared RAG service.
    rag_app.state.rag_service = RAGService(
        embedding_client=embedding_client,
        model_name="gemma4:e2b",
        top_k=5,
    )

    yield

    # Release resources when the application shuts down.
    del app.state.rag_service


app = FastAPI(lifespan=lifespan)

from app.api.chat import router as chat_router
from app.api.sessions import router as sessions_router

app.include_router(chat_router)
app.include_router(sessions_router)
