from pydantic import UUID4
from fastapi import Depends

from src.auth.tokens.dependencies import get_current_user as current_user
from src.core_.work_unit import UnitOfWork
from src.exceptions import PermissionDenied
from src.users.api_token.exceptions import ApiTokenByIdNotFound


async def can_access_token(
    token_id: UUID4,
    user: dict = Depends(current_user),
) -> None:
    uow = UnitOfWork()
    async with uow:
        token = await uow.api_tokens.get_by_id(
            entity_id=token_id,
        )
        
    if token is None:
        raise ApiTokenByIdNotFound()
    
    if token.user_id != user.user_id:
        raise PermissionDenied()
