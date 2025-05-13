from pydantic import SecretStr, UUID4

from src.auth.tokens import encode_jwt
from src.config.security.settings import REFRESH_TOKEN_EXPIRE_MINUTES


async def create_tokens_for_user(user_id: UUID4) -> dict[str, SecretStr]:
    access_token_payload = {"sub": str(user_id)}
    access_token = encode_jwt(payload=access_token_payload)

    refresh_token_payload = {"sub": str(user_id)}
    refresh_token = encode_jwt(
        payload=refresh_token_payload,
        expire_minutes=REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    # uow = UnitOfWork()
    # async with uow:
    #     await uow.users_tokens_pairs.create(
    #         data={
    #             "user_id": user_id,
    #             "access_token": access_token.get_secret_value(),
    #             "refresh_token": refresh_token.get_secret_value(),
    #             "is_actual": True,
    #         }
    #     )
    #
    #     await uow.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
