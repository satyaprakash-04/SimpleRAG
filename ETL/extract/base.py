from abc import ABC, abstractmethod
from typing import Any

from app.models.chunk import DocumentChunk
from uuid import UUID

from app.models.document import ExtractedDocument


class BaseExtractor(ABC):
    @abstractmethod
    def extract_paths(self, paths: str) -> list[str]:
        ...

    def extract_details(self,path: str) -> list[dict[str, Any]]:
        ...

class BaseFileReader(ABC):
    @abstractmethod
    def read(self, path) -> dict[str, Any]:
        ...


class BaseTransformer(ABC):
    @abstractmethod
    def transform(
            self,
            document: dict,
            document_id: UUID
    ) -> list[DocumentChunk]:
        ...


class BaseChunker(ABC):
    @abstractmethod
    def chunk(
            self,
            document: ExtractedDocument,
            document_id: UUID,
        ) -> list[DocumentChunk]:
        ...