from sqlalchemy import text

from ETL.load.load import BaseLoader
from app.models.document import Document
from app.models.chunk import DocumentChunkModel
from app.models.chunk import DocumentChunk as DocumentChunkData
from database.connector import SessionLocal


class PostgresLoader(BaseLoader):

    def load(
        self,
        document_id,
        file_name: str,
        file_path: str,
        extension: str,
        chunks: list[DocumentChunkData],
    ):
        session = SessionLocal()
        try:
            cleanup_query = text('truncate public.documents cascade;truncate public.document_chunks RESTART IDENTITY;')
            session.execute(cleanup_query)
            document = Document(
                id=document_id,
                file_name=file_name,
                file_path=file_path,
                extension=extension,
            )

            session.add(document)

            for chunk in chunks:

                if chunk.embedding is None:
                    raise ValueError(
                        f"Chunk {chunk.chunk_index} has no embedding"
                    )

                chunk_model = DocumentChunkModel(
                    document_id=document_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    metadata=chunk.metadata,
                    embedding=chunk.embedding,
                )

                session.add(chunk_model)

            session.commit()
            return document
        except Exception as e:
            session.rollback()
            print('error', e)
        finally:
            session.close()

