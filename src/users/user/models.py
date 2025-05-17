import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.infrastructure.database.database import Base
from src.users.user.schemas import UserSchema


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("user_id")

    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=True,
    )

    hashed_password: Mapped[bytes]

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now())

    # tokens_pair: Mapped[list["UserTokensPair"]] = relationship(
    #     # back_populates="user",
    #     cascade="all, delete, delete-orphan",
    #     lazy="selectin",
    # )

    def to_schema(self) -> UserSchema:
        return UserSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
