from app.clients.ollama_client import OllamaClient


class ChatService:

    def __init__(self):
        self.ollama_client = OllamaClient()

    async def generate_response(
        self,
        message: str
    ) -> str:

        response = await self.ollama_client.chat(
            message
        )

        return response