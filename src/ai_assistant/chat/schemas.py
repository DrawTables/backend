from src.core_.schemas import RequestModel


class ChatMessageRequestSchemas(RequestModel):
    request: str
    context: str | None = None


class ChatMessageResponseSchemas(RequestModel):
    response: str
