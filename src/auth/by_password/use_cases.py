from pydantic import EmailStr, SecretStr

from src.auth.by_password.service import is_valid_password
from src.auth.tokens.use_cases import create_tokens_for_user
from src.core_.work_unit import UnitOfWork
from src.users.user.schemas import UserSchema


async def login_by_username(
    username: str,
    password: SecretStr,
):
    uow = UnitOfWork()
    async with uow:
        users = await uow.users.get_by_filters(
            filter_by={"username": username},
        )

        if len(users) != 1:
            # TODO: Дописать условие!
            print(f"len(users) != 1")
            return

        user: UserSchema = users[0]
        if is_valid_password(
            plain_password=password,
            hashed_password=user.hashed_password,
        ):
            return await create_tokens_for_user(user_id=user.user_id)


async def login_by_email(
    email: EmailStr,
    password: SecretStr,
):
    uow = UnitOfWork()
    async with uow:
        users = await uow.users.get_by_filters(
            filter_by={"email": email},
        )

        if len(users) != 1:
            # TODO: Дописать условие!
            print(f"len(users) != 1")
            return

        user: UserSchema = users[0]
        if is_valid_password(
            plain_password=password,
            hashed_password=user.hashed_password,
        ):
            return await create_tokens_for_user(user_id=user.user_id)
