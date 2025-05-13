from fastapi import Response
from pydantic import SecretStr


def _get_public_token(token: SecretStr) -> SecretStr:
    return SecretStr(".".join(token.get_secret_value().split(".")[:2]))


def _get_private_token(token: SecretStr) -> SecretStr:
    return SecretStr(token.get_secret_value().split(".")[-1])


def set_tokens_to_cookies(
    response: Response,
    tokens_pair: dict[str, SecretStr],
):
    access_token = tokens_pair.get("access_token")
    refresh_token = tokens_pair.get("refresh_token")

    response.set_cookie(
        key="access-token",
        value=access_token.get_secret_value(),
        secure=True,
        samesite="none",
        httponly=True,
    )
    response.set_cookie(
        key="refresh-token",
        value=refresh_token.get_secret_value(),
        secure=True,
        samesite="none",
        httponly=True,
    )


def delete_tokens_from_cookies(response: Response):
    response.set_cookie(
        key="access-token",
        value="",
        expires="Thu, 01 Jan 1970 00:00:01 GMT",
    )
    response.set_cookie(
        key="refresh-token",
        value="",
        expires="Thu, 01 Jan 1970 00:00:01 GMT",
    )
