import uuid

from pydantic import UUID4

from src.core_.work_unit import UnitOfWork
from src.users.api_token.schemas import ApiTokenSchema


async def create_api_token(
    user_id: UUID4,
) -> ApiTokenSchema:
    uow = UnitOfWork()
    async with uow:
        token = str(uuid.uuid4().hex)
        await uow.api_tokens.add(
            data={
                "user_id": user_id,
                "token": token,
            }
        )
        await uow.commit()
        return token


async def delete_api_token(
    token_id: UUID4,
) -> None:
    uow = UnitOfWork()
    async with uow:
        await uow.api_tokens.delete_by_id(entity_id=token_id)


async def get_api_tokens(
    user_id: UUID4,
) -> list[ApiTokenSchema]:
    uow = UnitOfWork()
    async with uow:
        tokens = await uow.api_tokens.get_by_filters(filter_by={"user_id": user_id})
        return tokens
