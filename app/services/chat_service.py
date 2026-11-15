from langchain_core.messages import HumanMessage, AIMessage


class ChatService:
    def __init__(
        self,
        conversation_repository,
        vector_repository,
        rag_service,
    ):
        self.conversation_repository = conversation_repository
        self.vector_repository = vector_repository
        self.rag_service = rag_service

    async def stream_chat(
        self,
        session_id,
        question: str,
        history_limit: int = 10,
    ):
        conversation = (
            self.conversation_repository.get_by_session_id(
                session_id
            )
        )

        if conversation is None:
            raise ValueError("Conversation session not found")

        # Load history before storing the current question.
        previous_messages = (
            self.conversation_repository.get_recent_messages(
                conversation_id=conversation.id,
                limit=history_limit,
            )
        )

        chat_history = []

        for message in previous_messages:
            if message.role == "human":
                chat_history.append(
                    HumanMessage(content=message.content)
                )
            elif message.role == "ai":
                chat_history.append(
                    AIMessage(content=message.content)
                )

        # Save the current user message.
        self.conversation_repository.add_message(
            conversation_id=conversation.id,
            role="human",
            content=question,
        )

        yield {
            "type": "session",
            "data": {
                "session_id": str(session_id),
            },
        }

        full_response = []

        try:
            async for event in self.rag_service.stream_answer(
                question=question,
                chat_history=chat_history,
                vector_repository=self.vector_repository,
            ):
                if event["type"] == "token":
                    full_response.append(
                        event["data"]["content"]
                    )

                yield event

            # Persist the assistant response after successful generation.
            response = "".join(full_response)

            self.conversation_repository.add_message(
                conversation_id=conversation.id,
                role="ai",
                content=response,
            )

            yield {
                "type": "done",
                "data": {
                    "message": "Response completed",
                },
            }

        except Exception:
            # Log the exception in the application layer.
            raise
