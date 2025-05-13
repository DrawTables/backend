from src.auth.by_password.schemas import LoginRequest
from src.core_.work_unit import UnitOfWork
from src.users.user.exceptions import (
    UserByEmailNotFound,
    UserByUsernameNotFound,
)


async def user_by_username_or_email_exists(form_data: LoginRequest):
    uow = UnitOfWork()
    async with uow:
        if form_data.email is not None:
            users = await uow.users.get_by_filters(
                filter_by={"email": form_data.email},
            )
            if len(users) == 0:
                raise UserByEmailNotFound(email=form_data.email)

        if form_data.username is not None:
            users = await uow.users.get_by_filters(
                filter_by={"username": form_data.username},
            )
            if len(users) == 0:
                raise UserByUsernameNotFound(username=form_data.username)
