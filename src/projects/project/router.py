from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import UUID4

from src.auth.tokens.dependencies import get_current_user as current_user
from src.auth.tokens.dependencies import is_verified_user
from src.core_.pagination.dependencies import PaginationParamsDependency
from src.core_.pagination.schemas import PaginationResponse
from src.projects.project import use_cases
from src.projects.project.dependencies import (
    project_by_id_exists,
    user_can_change_project,
)
from src.projects.project.schemas import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
    ProjectUserPermissionsRequest,
    ProjectPullRequest,
    ProjectPullResponse,
)

ROUTER_V1_PREFIX = "/api/v1/projects"

projects_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Projects v1"],
    dependencies=[Depends(is_verified_user)],
)


@projects_router_v1.get(
    path="",
    response_model=PaginationResponse[ProjectResponse],
)
async def get_projects(
    pagination_params: PaginationParamsDependency,
    user_id: UUID4 = Query(default=None, alias="userId"),
    user: dict = Depends(current_user),
) -> PaginationResponse[ProjectResponse]:
    request_user_id = user.user_id
    amount, projects = await use_cases.get_projects(
        pagination_params=pagination_params,
        user_id=user_id,
        request_user_id=request_user_id,
    )
    return {
        "entities": projects,
        "entities_amount": amount,
    }


@projects_router_v1.get(
    path="/pull",
    response_model=ProjectPullResponse,
)
async def pull_project(
    body: ProjectPullRequest,
):
    dbml_text = await use_cases.get_project_by_pull_request(
        project_url=body.project_url,
        api_key=body.api_key,
    )
    return ProjectPullResponse(dbml=dbml_text)


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
    dependencies=[Depends(project_by_id_exists), Depends(user_can_change_project)],
)
async def update_project(
    project_id: str,
    project_update_request: ProjectUpdateRequest,
):
    await use_cases.update_project(project_id, project_update_request)


@projects_router_v1.put(
    path="/{project_id}/users",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(project_by_id_exists), Depends(user_can_change_project)],
)
async def add_user_to_project(
    project_id: str,
    body: ProjectUserPermissionsRequest,
    user: dict = Depends(current_user),
):
    await use_cases.change_user_permissions(project_id, body)


@projects_router_v1.delete(
    path="/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(project_by_id_exists), Depends(user_can_change_project)],
)
async def delete_project(
    project_id: str,
):
    await use_cases.delete_project(project_id)
