from sentence_transformers import SentenceTransformer

from .embedding_client import EmbeddingClient


class SentenceTransformerClient(EmbeddingClient):

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=16,
            show_progress_bar=False,
        )

        return embeddings.tolist()