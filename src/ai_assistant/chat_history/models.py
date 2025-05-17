import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.ai_assistant.chat_history.schemas import AssistantChatMessageSchema
from src.infrastructure.database.database import Base


class AssistantChatMessage(Base):
    __tablename__ = "assistant_chat_message"

    assistant_chat_message_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("assistant_chat_message_id")
    project_id: Mapped[UUID4] = mapped_column(
        ForeignKey("project.project_id", ondelete="CASCADE"),
        index=True,
    )
    user_message: Mapped[str]
    assistant_message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def to_schema(self) -> AssistantChatMessageSchema:
        return AssistantChatMessageSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
