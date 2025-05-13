from fastapi import APIRouter, Depends, Response, status

from src.auth.tokens.dependencies import (
    get_current_user as current_user,
    is_verified_user,
)
from src.users.user import use_cases
from src.users.user.dependencies import user_by_username_or_email_not_exists
from src.users.user.schemas import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)

ROUTER_V1_PREFIX = "/api/v1/users"

router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Users v1"],
)


@router_v1.get(
    path="/me",
    response_model=UserResponse,
    dependencies=[Depends(is_verified_user)],
)
async def get_current_user(user=Depends(current_user)):
    return user


@router_v1.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(user_by_username_or_email_not_exists)],
)
async def create_user(
    body: UserCreateRequest,
    response: Response,
):
    user_id = await use_cases.create_user(body=body)
    location = f"{ROUTER_V1_PREFIX}/{user_id}"
    response.headers["Location"] = location


@router_v1.patch(
    path="/me",
    dependencies=[Depends(is_verified_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_current_user(
    body: UserUpdateRequest,
    user=Depends(current_user),
):
    await use_cases.update_current_user(
        user_id=user.user_id,
        body=body,
    )
