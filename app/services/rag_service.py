from app.clients.embedding_client import EmbeddingClient


class RAGService:

    def __init__(
        self,
        embedding_client: EmbeddingClient,
        vector_repository,
    ):
        self.embedding_client = embedding_client
        self.vector_repository = vector_repository

    def create_query_embedding(self, query: str) -> list[float]:
        return self.embedding_client.embed(query)

    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_client.embed(query)

        return self.vector_repository.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )