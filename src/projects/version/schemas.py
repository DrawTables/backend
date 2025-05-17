from datetime import datetime

from pydantic import UUID4, Field

from src.core_.schemas import RequestModel, ResponseModel, SchemaModel


class VersionSchema(SchemaModel):
    version_id: UUID4
    project_id: UUID4
    tag: str | None = Field(default=None)
    dbml_text: str
    parent_id: UUID4 | None = Field(default=None)
    created_at: datetime


class VersionCreateSchema(RequestModel):
    tag: str | None = Field(default=None)
    dbml_text: str


class VersionUpdateSchema(RequestModel):
    tag: str | None = Field(default=None)
    dbml_text: str | None = Field(default=None)


class VersionResponseSchema(ResponseModel):
    version_id: UUID4
    project_id: UUID4
    tag: str | None = Field(default=None)
    parent_id: UUID4 | None = Field(default=None)
    created_at: datetime
    
    
class VersionResponseExtendedSchema(ResponseModel):
    dbml_text: str