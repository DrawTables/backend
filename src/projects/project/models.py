import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import func, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.infrastructure.database.database import Base
from src.projects.project.schemas import ProjectSchema

class Project(Base):
    __tablename__ = "project"

    project_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("project_id")

    title: Mapped[str]
    description: Mapped[str]
    owner_user_id: Mapped[UUID4] = mapped_column(
        ForeignKey(
            "user.user_id", ondelete="CASCADE"
        ),
        index=True,
    )
    
    def to_schema(self) -> ProjectSchema:
        return ProjectSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
