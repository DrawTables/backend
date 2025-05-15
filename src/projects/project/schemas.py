from datetime import datetime

from pydantic import  Field, UUID4

from src.core_.schemas import SchemaModel, RequestModel, ResponseModel


class ProjectSchema(SchemaModel):
    project_id: UUID4
    title: str
    description: str
    owner_user_id: UUID4


class ProjectResponse(ProjectSchema, ResponseModel):
    pass


class ProjectCreateRequest(RequestModel):
    title: str
    description: str


class ProjectUpdateRequest(RequestModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
