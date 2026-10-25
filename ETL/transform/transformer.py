from app.models.document import ExtractedDocument
from app.models.chunk import DocumentChunk
from uuid import UUID

from .cleaner import TextCleaner
from ..extract.base import BaseTransformer, BaseChunker


class DocumentTransformer(BaseTransformer):

    def __init__(
        self,
        cleaner: TextCleaner,
        chunker: BaseChunker,
    ):
        self.cleaner = cleaner
        self.chunker = chunker

    def transform(
        self,
        document: dict,
        document_id: UUID,
    ) -> list[DocumentChunk]:
        cleaned_text = self.cleaner.clean(
            document['page_data']
        )

        cleaned_document = ExtractedDocument(
            file_path=document['file_path'],
            file_name=document['file_name'],
            extension=document['extension'],
            page_start=document['page_start'],
            page_end=document['page_end'],
            text=cleaned_text,
        )

        return self.chunker.chunk(
            cleaned_document,
            document_id,
        )