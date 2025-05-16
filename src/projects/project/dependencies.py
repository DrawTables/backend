from pydantic import UUID4
from fastapi import Depends

from src.auth.tokens.dependencies import get_current_user as current_user
from src.core_.work_unit import UnitOfWork
from src.projects.project.exceptions import ProjectByIdNotFound
from src.exceptions import PermissionDenied


async def project_by_id_exists(project_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        project = await uow.projects.get_by_id(entity_id=project_id)

    if project is None:
        raise ProjectByIdNotFound(project_id=project_id)


async def user_can_change_project(
    project_id: UUID4,
    user: dict = Depends(current_user),
):
    uow = UnitOfWork()
    async with uow:
        project = await uow.projects.get_by_id(entity_id=project_id)
        if project is None:
            raise ProjectByIdNotFound(project_id=project_id)
        if project.owner_user_id != user.user_id:
            raise PermissionDenied()