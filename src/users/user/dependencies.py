from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.users.user.exceptions import (
    UserByEmailAlreadyExists,
    UserByIdNotFound,
    UserByUsernameAlreadyExists,
)
from src.users.user.schemas import UserCreateRequest


async def user_by_id_exists(user_id: UUID4):
    uow = UnitOfWork()
    async with uow:
        user = await uow.users.get_by_id(entity_id=user_id)

    if user is None:
        raise UserByIdNotFound(user_id=user_id)


async def user_by_username_or_email_not_exists(body: UserCreateRequest):
    uow = UnitOfWork()
    async with uow:
        if body.email is not None:
            users = await uow.users.get_by_filters(
                filter_by={"email": body.email},
            )
            if len(users) > 0:
                raise UserByEmailAlreadyExists(email=body.email)

        if body.username is not None:
            users = await uow.users.get_by_filters(
                filter_by={"username": body.username},
            )
            if len(users) > 0:
                raise UserByUsernameAlreadyExists(username=body.username)
