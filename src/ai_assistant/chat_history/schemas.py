from datetime import datetime

from pydantic import UUID4

from src.core_.schemas import RequestModel, ResponseModel, SchemaModel


class AssistantChatMessageSchema(SchemaModel):
    assistant_chat_message_id: UUID4
    project_id: UUID4
    user_message: str
    assistant_message: str
    created_at: datetime


class AssistantChatMessageCreateSchema(RequestModel):
    user_message: str
    assistant_message: str


class AssistantChatMessageResponseSchema(AssistantChatMessageSchema, ResponseModel):
    pass
