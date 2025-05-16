from src.core_.schemas import RequestModel


class ChatMessageRequestSchemas(RequestModel):
    request: str
    

class ChatMessageResponseSchemas(RequestModel):
    response: str