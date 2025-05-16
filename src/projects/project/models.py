import uuid

from pydantic import UUID4
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.infrastructure.database.database import Base
from src.projects.project.schemas import ProjectRealtionUserSchema, ProjectSchema


class ProjectRealtionUser(Base):
    __tablename__ = "project_relation_user"

    relation_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id = synonym("relation_id")

    project_id: Mapped[UUID4] = mapped_column(
        ForeignKey("project.project_id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[UUID4] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        index=True,
    )
    read_permission: Mapped[bool] = mapped_column(
        default=False,
    )
    write_permission: Mapped[bool] = mapped_column(
        default=False,
    )

    def to_schema(self) -> ProjectRealtionUserSchema:
        return ProjectRealtionUserSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()


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
        ForeignKey("user.user_id", ondelete="CASCADE"),
        index=True,
    )

    private: Mapped[bool] = mapped_column(
        default=False,
    )

    def to_schema(self) -> ProjectSchema:
        return ProjectSchema.model_validate(self)

    def to_dict(self) -> dict:
        return self.to_schema().model_dump()
