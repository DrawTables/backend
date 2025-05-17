from src.core_.repository import SQLAlchemyRepository
from src.ai_assistant.chat_history.models import AssistantChatMessage


class AssistantChatMessageRepository(SQLAlchemyRepository):
    _model = AssistantChatMessage
