from app.clients.embedding_client import EmbeddingClient
from app.models.chunk import DocumentChunk


class DocumentEmbedder:

    def __init__(self, embedding_client: EmbeddingClient):
        self.embedding_client = embedding_client

    def embed(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        if not chunks:
            return []

        texts = [chunk.content for chunk in chunks]

        embeddings = self.embedding_client.embed_batch(texts)

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings do not match"
            )

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        return chunks