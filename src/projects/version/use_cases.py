from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.projects.version.schemas import (
    VersionCreateSchema,
    VersionResponseSchema,
    VersionUpdateSchema,
)


async def get_versions(
    project_id: UUID4,
) -> list[VersionResponseSchema]:
    uow = UnitOfWork()
    async with uow:
        versions = await uow.versions.get_by_filters(
            filter_by={
                "project_id": project_id,
            },
        )

    return versions


async def create_version(
    project_id: UUID4,
    body: VersionCreateSchema,
) -> UUID4:
    uow = UnitOfWork()
    data = body.model_dump()
    data["project_id"] = project_id
    async with uow:
        version_id: UUID4 = await uow.versions.create(data=data)
        await uow.commit()

    return version_id


async def update_version(
    version_id: UUID4,
    body: VersionUpdateSchema,
):
    uow = UnitOfWork()
    data = body.model_dump()
    async with uow:
        await uow.versions.update(entity_id=version_id, data=data)
        await uow.commit()


async def delete_version(
    version_id: UUID4,
):
    uow = UnitOfWork()

    async with uow:
        await uow.versions.delete(entity_id=version_id)
        await uow.commit()
