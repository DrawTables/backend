import uuid
from datetime import datetime

from pydantic import UUID4
from sqlalchemy import UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.infrastructure.database.database import Base
from src.projects.version.schemas import VersionSchema


class Version(Base):
    __tablename__ = "version"

    version_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("version_id")
    project_id: Mapped[UUID4] = mapped_column(
        ForeignKey("project.project_id", ondelete="CASCADE"),
        index=True,
    )

    tag: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
    )
    dbml_text: Mapped[str]
    parent_id: Mapped[UUID4] = mapped_column(
        ForeignKey("version.version_id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def to_schema(self) -> VersionSchema:
        return VersionSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
