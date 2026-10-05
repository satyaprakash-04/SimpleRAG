import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class OllamaClient:

    def __init__(self):
        self.base_url = os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434"
        )

        self.model = os.getenv(
            "MODEL_NAME",
            "gemma4:e2b"
        )

    async def chat(self, message: str) -> str:

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False,
            "options": {
                "num_predict": 512
            }
        }

        async with httpx.AsyncClient(
            timeout=600
        ) as client:

            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )

            response.raise_for_status()

            data = response.json()

            return data["message"]["content"]