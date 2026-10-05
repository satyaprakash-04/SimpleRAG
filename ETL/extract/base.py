from abc import ABC, abstractmethod

from app.models.chunk import DocumentChunk
from uuid import UUID

from app.models.document import ExtractedDocument


class BaseExtractor(ABC):
    @abstractmethod
    def extract_paths(self, paths: str) -> list[str]:
        ...

    def extract_details(self,path: str) -> list[dict[str, str | list[dict[str, str]]]]:
        ...

class BaseFileReader(ABC):
    @abstractmethod
    def read(self, path) -> list[dict[str, str]]:
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