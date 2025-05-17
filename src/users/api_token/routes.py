from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from src.auth.tokens.dependencies import get_current_user as current_user
from src.auth.tokens.dependencies import is_verified_user
from src.users.api_token import use_cases
from src.users.api_token.dependencies import can_access_token
from src.users.api_token.schemas import ApiTokenCreateResponse, ApiTokenResponse

ROUTER_V1_PREFIX = "/api/v1/api-tokens"

api_tokens_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Api-Tokens v1"],
    dependencies=[Depends(is_verified_user)],
)


@api_tokens_router_v1.get(
    path="",
    response_model=list[ApiTokenResponse],
)
async def get_api_tokens(
    user: dict = Depends(current_user),
) -> list[ApiTokenResponse]:
    user_id = user.user_id
    tokens = await use_cases.get_api_tokens(
        user_id=user_id,
    )
    return tokens


@api_tokens_router_v1.post(
    path="",
    response_model=ApiTokenCreateResponse,
)
async def create_api_token(
    user: dict = Depends(current_user),
) -> ApiTokenCreateResponse:
    user_id = user.user_id
    token = await use_cases.create_api_token(
        user_id=user_id,
    )
    return {
        "token": token,
    }


@api_tokens_router_v1.delete(
    path="/{token_id}",
    dependencies=[Depends(can_access_token)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_api_token(
    token_id: UUID4,
):
    await use_cases.delete_api_token(
        token_id=token_id,
    )
