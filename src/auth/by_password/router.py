from typing import Annotated

from fastapi import APIRouter, Form, Depends, Response, status

from src.auth.by_password import use_cases
from src.auth.by_password.dependencies import user_by_username_or_email_exists
from src.auth.by_password.schemas import LoginRequest
from src.auth.tokens.utils import (
    delete_tokens_from_cookies,
    set_tokens_to_cookies,
)

ROUTER_V1_PREFIX = "/api/v1/auth"

router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Auth v1"],
)


@router_v1.post(
    path="/login",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_by_username_or_email_exists)],
)
async def login(
    form_data: Annotated[LoginRequest, Form()],
    response: Response,
):
    tokens_pair = None
    if form_data.username is not None:
        tokens_pair = await use_cases.login_by_username(
            username=form_data.username,
            password=form_data.password,
        )

    elif form_data.email is not None:
        tokens_pair = await use_cases.login_by_email(
            email=form_data.email,
            password=form_data.password,
        )

    if tokens_pair is not None:
        set_tokens_to_cookies(
            response=response,
            tokens_pair=tokens_pair,
        )
        return

    delete_tokens_from_cookies(response=response)
    response.status_code = status.HTTP_401_UNAUTHORIZED


@router_v1.get(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(response: Response):
    delete_tokens_from_cookies(response=response)
