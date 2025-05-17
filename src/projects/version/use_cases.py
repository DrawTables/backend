from datetime import datetime

from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.projects.version.schemas import (
    VersionCreateSchema,
    VersionResponseSchema,
    VersionUpdateSchema,
)
from src.projects.version.models import Version

async def get_versions(
    project_id: UUID4,
) -> list[VersionResponseSchema]:
    uow = UnitOfWork()
    async with uow:
        versions = await uow.versions.get_by_filters(
            filter_by={
                "project_id": project_id,
            },
            order_by=Version.created_at.desc(),
        )

    return versions


async def get_version(
    version_id: UUID4,
) -> VersionResponseSchema:
    uow = UnitOfWork()
    async with uow:
        version = await uow.versions.get_by_id(
            entity_id=version_id,
        )

    return version


async def create_version(
    project_id: UUID4,
    body: VersionCreateSchema,
) -> UUID4:
    uow = UnitOfWork()
    data = body.model_dump()
    data["project_id"] = project_id

    async with uow:
        last_version = await uow.versions.get_by_filters(
            filter_by={
                "project_id": project_id,
                "tag": "latest",
            },
        )

        if not last_version:
            if body.tag is None:
                data["tag"] = "latest"
            new_version_id = await uow.versions.add(
                data={
                    **data,
                    "parent_id": None,
                },
            )
            if body.tag is not None:
                await uow.versions.add(
                    data={
                        "project_id": project_id,
                        "tag": "latest",
                        "dbml_text": body.dbml_text,
                        "tables_coordinates": body.tables_coordinates,
                        "colors": body.colors,
                        "parent_id": new_version_id,
                    },
                )
            await uow.commit()
            return new_version_id

        if body.tag is None:
            new_version_id = await uow.versions.update_by_id(
                data={
                    **data,
                    "parent_id": last_version[0].parent_id if last_version else None,
                    "created_at": datetime.now(),
                },
                entity_id=last_version[0].version_id,
            )
        else:
            new_version_id = await uow.versions.add(
                data={
                    **data,
                    "parent_id": last_version[0].parent_id,
                },
            )
            await uow.versions.update_by_id(
                data={
                    "parent_id": new_version_id,
                    "created_at": datetime.now(),
                },
                entity_id=last_version[0].version_id,
            )

        await uow.commit()

    return new_version_id


async def update_version(
    version_id: UUID4,
    body: VersionUpdateSchema,
):
    uow = UnitOfWork()
    data = body.model_dump()
    async with uow:
        await uow.versions.update(entity_id=version_id, data=data)
        await uow.commit()


async def delete_last_version(
    project_id: UUID4,
):
    uow = UnitOfWork()

    async with uow:
        last_version = await uow.versions.get_by_filters(
            filter_by={
                "project_id": project_id,
                "tag": "latest",
            },
        )
        if last_version:
            await uow.versions.delete(entity_id=last_version[0].parent_id)
        await uow.commit()
