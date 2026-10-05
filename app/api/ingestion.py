from fastapi import APIRouter
from app.services.ingestion_service import  IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/")
def ingest(source: str):
    ingestion_service = IngestionService()

    ingestion_service.ingest(source)

    return {
        "message": "Ingestion completed"
    }