import uuid

from pydantic import UUID4
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.infrastructure.database.database import Base
from src.users.api_token.schemas import ApiTokenSchema


class ApiToken(Base):
    __tablename__ = "api_token"

    api_token_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("api_token_id")

    user_id: Mapped[UUID4] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        index=True,
    )
    token: Mapped[str]


    def to_schema(self) -> ApiTokenSchema:
        return ApiTokenSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
