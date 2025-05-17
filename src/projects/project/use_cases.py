from pydantic import UUID4

from src.core_.pagination.schemas import PaginationParams
from src.core_.specifications import Specification
from src.core_.work_unit import UnitOfWork
from src.projects.project.schemas import (
    ProjectCreateRequest,
    ProjectSchema,
    ProjectUpdateRequest,
    ProjectUserPermissionsRequest,
)
from src.projects.project.specifications import (
    ProjectByOwnerIdSpecification,
    ProjectsUserHasAccessSpecification,
)


async def get_project_by_id(project_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        return await uow.projects.get_by_id(entity_id=project_id)


async def get_projects(
    pagination_params: PaginationParams | None = None,
    user_id: UUID4 | None = None,
    request_user_id: UUID4 | None = None,
) -> tuple[int, list[ProjectSchema]]:
    uow = UnitOfWork()
    specification = Specification()

    if user_id:
        specification &= ProjectByOwnerIdSpecification(user_id=user_id)

    if request_user_id:
        specification &= ProjectsUserHasAccessSpecification(user_id=request_user_id)

    async with uow:
        projects = await uow.projects.get_by_filters(
            specification=specification,
            pagination=pagination_params,
        )
        amount = await uow.projects.amount(
            specification=specification,
        )

    return amount, projects


async def create_project(body: ProjectCreateRequest, owner_user_id: UUID4) -> UUID4:
    uow = UnitOfWork()
    data = body.model_dump()
    data["owner_user_id"] = owner_user_id
    async with uow:
        project_id: UUID4 = await uow.projects.create(data=data)
        await uow.commit()

    return project_id


async def update_project(
    project_id: UUID4,
    body: ProjectUpdateRequest,
):
    uow = UnitOfWork()
    async with uow:
        await uow.projects.update_by_id(
            entity_id=project_id,
            data=body.model_dump(),
        )
        await uow.commit()


async def delete_project(project_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        await uow.projects.delete_by_id(entity_id=project_id)
        await uow.commit()


async def change_user_permissions(
    project_id: UUID4,
    body: ProjectUserPermissionsRequest,
):
    uow = UnitOfWork()
    data = body.model_dump()
    data["project_id"] = project_id
    async with uow:
        if body.read_permission is False and body.write_permission is False:
            await uow.projects_relation_users.delete(
                filter_by={
                    "project_id": project_id,
                    "user_id": body.user_id,
                }
            )
        else:
            await uow.projects_relation_users.upsert(
                data=data,
                filter_by={
                    "project_id": project_id,
                    "user_id": body.user_id,
                },
            )
        await uow.commit()


async def get_project_by_pull_request(
    project_url: str,
    api_key: str,
) -> ProjectSchema:
    uow = UnitOfWork()
    async with uow:
        username, project_name = project_url.split("/")[-2:]
        user = await uow.users.get_by_filters(
            filter_by={"username": username},
        )
        api_key = await uow.api_tokens.get_by_filters(
            filter_by={
                "user_id": user[0].user_id,
                "token": api_key,
            },
        )
        if not api_key:
            raise Exception("API key not found")
        project = await uow.projects.get_by_filters(
            filter_by={
                "title": project_name,
                "owner_user_id": user[0].user_id,
            },
        )

        last_version = await uow.versions.get_by_filters(
            filter_by={
                "project_id": project[0].project_id,
                "tag": "latest",
            },
        )
        return last_version[0].dbml_text
