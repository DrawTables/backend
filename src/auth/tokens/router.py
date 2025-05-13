from fastapi import APIRouter, Depends, Response, status

from src.auth.tokens.dependencies import get_current_user
from src.auth.tokens.use_cases import create_tokens_for_user
from src.auth.tokens.utils import set_tokens_to_cookies

ROUTER_V1_PREFIX = "/api/v1/tokens"

router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Tokens v1"],
)


@router_v1.get(
    path="/refresh",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def refresh(
    response: Response,
    user=Depends(get_current_user),
):
    tokens_pair = await create_tokens_for_user(
        user_id=user.user_id,
    )
    set_tokens_to_cookies(
        response=response,
        tokens_pair=tokens_pair,
    )
