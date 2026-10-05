import os

from fastapi import FastAPI

from app.api.chat import router as chat_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI(
    title="Gemma 4 API",
    version="1.0.0"
)


app.include_router(chat_router)


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }