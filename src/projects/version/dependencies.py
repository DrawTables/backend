from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.projects.version.exceptions import VersionByIdNotFound


async def version_by_id_exists(version_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        project = await uow.versions.get_by_id(entity_id=version_id)

    if project is None:
        raise VersionByIdNotFound(version_id=version_id)
