from fastapi import Request
from pydantic import SecretStr

from src.auth.tokens import decode_jwt
from src.core_.work_unit import UnitOfWork
from src.exceptions import NotAuthenticated
from src.users.user.schemas import UserSchema


def _get_access_token_info_from_request(request: Request):
    access_token = request.cookies.get("access-token")

    if access_token is None:
        print("Invalid tokens. Not access_token!!!")

    access_token = SecretStr(access_token)
    access_token_info = decode_jwt(token=access_token)

    if access_token_info is None:
        # TODO: Обработка случая, когда не валидные токены!
        print("Invalid tokens!!!")
        raise NotAuthenticated

    return access_token_info


async def get_current_user(request: Request) -> UserSchema:
    access_token_info = _get_access_token_info_from_request(request=request)
    user_id = access_token_info.get("sub")
    uow = UnitOfWork()
    async with uow:
        users = await uow.users.get_by_filters(
            filter_by={"user_id": user_id},
        )

    return users[0]


async def is_verified_user(request: Request):
    access_token_info = _get_access_token_info_from_request(request=request)
    user_id = access_token_info.get("sub")
    if user_id is None:
        raise NotAuthenticated()
