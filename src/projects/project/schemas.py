from pydantic import UUID4, Field

from src.core_.schemas import RequestModel, ResponseModel, SchemaModel


class ProjectSchema(SchemaModel):
    project_id: UUID4
    title: str
    description: str
    owner_user_id: UUID4
    private: bool


class ProjectResponse(ProjectSchema, ResponseModel):
    pass


class ProjectCreateRequest(RequestModel):
    title: str
    description: str
    private: bool


class ProjectUpdateRequest(RequestModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    private: bool | None = Field(default=None)


class ProjectRealtionUserSchema(SchemaModel):
    relation_id: UUID4
    project_id: UUID4
    user_id: UUID4
    read_permission: bool = Field(default=False)
    write_permission: bool = Field(default=False)


class ProjectUserPermissionsRequest(RequestModel):
    user_id: UUID4
    read_permission: bool = Field(default=True)
    write_permission: bool = Field(default=False)


class ProjectPullRequest(RequestModel):
    project_url: UUID4
    api_key: UUID4


class ProjectPullResponse(ResponseModel):
    dbml: str
