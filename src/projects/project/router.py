from fastapi import APIRouter, Depends, Response, status

from src.auth.tokens.dependencies import (
    get_current_user as current_user,
)
from src.projects.project import use_cases
from src.projects.project.dependencies import project_by_id_exists
from src.projects.project.schemas import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)

ROUTER_V1_PREFIX = "/api/v1/projects"

projects_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Projects v1"],
)


@projects_router_v1.get(
    path="/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Depends(project_by_id_exists)],
)
async def get_project(
    project_id: str,
) -> ProjectResponse:
    return await use_cases.get_project_by_id(project_id)


@projects_router_v1.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_create_request: ProjectCreateRequest,
    response: Response,
    user: dict = Depends(current_user),
):
    project_id = await use_cases.create_project(project_create_request, user.user_id)
    response.headers["Location"] = f"{ROUTER_V1_PREFIX}/{project_id}"


@projects_router_v1.patch(
    path="/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(project_by_id_exists)],
)
async def update_project(
    project_id: str,
    project_update_request: ProjectUpdateRequest,
):
    await use_cases.update_project(project_id, project_update_request)


@projects_router_v1.delete(
    path="/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(project_by_id_exists)],
)
async def delete_project(
    project_id: str,
):
    await use_cases.delete_project(project_id)
