from datetime import datetime, timezone

from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.projects.project.schemas import ProjectCreateRequest, ProjectUpdateRequest


async def get_project_by_id(project_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        return await uow.projects.get_by_id(entity_id=project_id)


async def get_projects():
    uow = UnitOfWork()
    async with uow:
        return await uow.projects.get_by_filters()


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