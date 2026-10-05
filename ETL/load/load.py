from abc import ABC, abstractmethod
from app.models.chunk import DocumentChunk as DocumentChunkData

class BaseLoader(ABC):
    @abstractmethod
    def load(self,document_id,
        file_name: str,
        file_path: str,
        extension: str,
        chunks: list[DocumentChunkData],):
        ...