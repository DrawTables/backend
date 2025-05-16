from fastapi import Depends, Query
from pydantic import UUID4

from src.auth.tokens.dependencies import get_current_user as current_user
from src.core_.work_unit import UnitOfWork
from src.exceptions import PermissionDenied
from src.projects.project.exceptions import ProjectByIdNotFound


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


async def user_have_read_access_to_project(
    project_id: UUID4 = Query(default=None, alias="projectId"),
    user: dict = Depends(current_user),
):
    uow = UnitOfWork()
    async with uow:
        project = await uow.projects.get_by_id(entity_id=project_id)
        if project is None:
            raise ProjectByIdNotFound(project_id=project_id)
        if project.owner_user_id == user.user_id:
            return

        project_relation = await uow.projects_relation_users.get_by_filters(
            filter_by={
                "user_id": user.user_id,
                "project_id": project_id,
            }
        )
        if project_relation is None:
            raise PermissionDenied()


async def user_have_write_access_to_project(
    project_id: UUID4 = Query(default=None, alias="projectId"),
    user: dict = Depends(current_user),
):
    uow = UnitOfWork()
    async with uow:
        project = await uow.projects.get_by_id(entity_id=project_id)
        if project is None:
            raise ProjectByIdNotFound(project_id=project_id)
        if project.owner_user_id == user.user_id:
            return

        project_relation = await uow.projects_relation_users.get_by_filters(
            filter_by={
                "user_id": user.user_id,
                "project_id": project_id,
            }
        )
        if project_relation is None or len(project_relation) == 0:
            raise PermissionDenied()
        project_relation = project_relation[0]
        if project_relation.write_permission is False:
            raise PermissionDenied()
