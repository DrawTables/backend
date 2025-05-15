from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.projects.project.exceptions import (
    ProjectByIdNotFound
)
from src.projects.project.schemas import ProjectCreateRequest


async def project_by_id_exists(project_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        project = await uow.projects.get_by_id(entity_id=project_id)

    if project is None:
        raise ProjectByIdNotFound(project_id=project_id)

