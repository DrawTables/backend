from src.ai_assistant.chat_history.models import AssistantChatMessage
from src.core_.repository import SQLAlchemyRepository


class AssistantChatMessageRepository(SQLAlchemyRepository):
    _model = AssistantChatMessage
