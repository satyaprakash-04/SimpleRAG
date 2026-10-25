from ETL.extract.base import BaseChunker
from app.models.document import ExtractedDocument
from app.models.chunk import DocumentChunk
from uuid import UUID


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        chunk_size: int = 3000,
        chunk_overlap: int = 500,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ]

    def chunk(
        self,
        document: ExtractedDocument,
        document_id: UUID,
    ) -> list[DocumentChunk]:

        text = document.text.strip()

        if not text:
            return []

        chunks = self._split_text(
            text,
            self.separators,
        )

        return [
            DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk,
                file_path=document.file_path,
                file_name=document.file_name,
                page_start=document.page_start,
                page_end=document.page_end,
            )
            for index, chunk in enumerate(chunks)
        ]

    def _split_text(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text]

        if not separators:
            return self._split_by_size(text)

        separator = separators[0]

        if separator:
            parts = text.split(separator)
        else:
            return self._split_by_size(text)

        chunks = []

        current = ""

        for part in parts:

            part = part.strip()

            if not part:
                continue

            candidate = (
                f"{current}{separator}{part}"
                if current
                else part
            )

            if len(candidate) <= self.chunk_size:

                current = candidate

            else:

                if current:
                    chunks.append(current)

                if len(part) <= self.chunk_size:
                    current = part

                else:
                    sub_chunks = self._split_text(
                        part,
                        separators[1:],
                    )

                    chunks.extend(sub_chunks)

                    current = ""

        if current:
            chunks.append(current)

        return self._add_overlap(chunks)

    def _split_by_size(
        self,
        text: str,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = min(
                start + self.chunk_size,
                len(text),
            )

            chunks.append(
                text[start:end]
            )

            start = (
                end - self.chunk_overlap
            )

        return chunks

    def _add_overlap(
        self,
        chunks: list[str],
    ) -> list[str]:

        if not chunks:
            return []

        result = [chunks[0]]

        for chunk in chunks[1:]:

            previous = result[-1]

            overlap = previous[
                -self.chunk_overlap:
            ]

            result.append(
                f"{overlap} {chunk}"
            )

        return result