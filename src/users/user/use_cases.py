from pydantic import UUID4

from src.auth.by_password.service import get_hashed_password
from src.core_.work_unit import UnitOfWork
from src.users.user.schemas import UserCreateRequest, UserUpdateRequest


async def get_user_by_id(user_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        return await uow.users.get_by_id(entity_id=user_id)


async def get_users():
    uow = UnitOfWork()
    async with uow:
        return await uow.users.get_by_filters()


async def create_user(body: UserCreateRequest) -> UUID4:
    uow = UnitOfWork()
    async with uow:
        hashed_password = get_hashed_password(body.password)
        data: dict = body.model_dump()
        data.pop("password", None)
        data["hashed_password"] = hashed_password.get_secret_value()

        user_id: UUID4 = await uow.users.create(data=data)
        await uow.commit()

    return user_id


async def update_current_user(
    user_id: UUID4,
    body: UserUpdateRequest,
):
    uow = UnitOfWork()
    async with uow:
        await uow.users.update_by_id(
            entity_id=user_id,
            data=body.model_dump(),
        )
        await uow.commit()
