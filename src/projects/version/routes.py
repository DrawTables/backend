from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4

from src.auth.tokens.dependencies import is_verified_user
from src.projects.project.dependencies import (
    user_have_read_access_to_project,
    user_have_write_access_to_project,
)
from src.projects.version import use_cases
from src.projects.version.dependencies import version_by_id_exists
from src.projects.version.schemas import VersionCreateSchema, VersionResponseSchema

ROUTER_V1_PREFIX = "/api/v1/projects/versions"

versions_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Projects-Versions v1"],
    dependencies=[Depends(is_verified_user)],
)


@versions_router_v1.get(
    path="",
    response_model=list[VersionResponseSchema],
    dependencies=[
        Depends(user_have_read_access_to_project),
    ],
)
async def get_versions(
    project_id: UUID4 = Query(default=None, alias="projectId"),
) -> list[VersionResponseSchema]:
    versions = await use_cases.get_versions(
        project_id=project_id,
    )
    return versions


@versions_router_v1.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(user_have_write_access_to_project),
    ],
)
async def create_version(
    body: VersionCreateSchema,
    response: Response,
    project_id: UUID4 = Query(default=None, alias="projectId"),
):
    version_id = await use_cases.create_version(
        project_id=project_id,
        body=body,
    )
    response.headers["Location"] = f"{ROUTER_V1_PREFIX}/{version_id}"


@versions_router_v1.patch(
    path="/{version_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(version_by_id_exists),
        Depends(user_have_write_access_to_project),
    ],
)
async def update_version(
    version_id: UUID4,
    body: VersionCreateSchema,
):
    await use_cases.update_version(
        version_id=version_id,
        body=body,
    )
