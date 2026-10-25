from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunkModel


class VectorRepository:

    def __init__(self, session: Session):
        self.session = session

    def similarity_search(
            self,
            query_embedding: list[float],
            top_k: int = 5
    ) -> list[DocumentChunkModel]:
        statement = (
            select(DocumentChunkModel)
            .where(DocumentChunkModel.embedding.is_not(None))
            .order_by(
                DocumentChunkModel.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(top_k)
        )

        return list(
            self.session.execute(statement).scalars().all()
        )
