from datetime import datetime, timedelta
from pathlib import Path

import jwt
from pydantic import SecretStr

from src.config.security.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    CERTS_DIR_PATH,
    JWT_ALGORITHM,
    JWT_PRIVATE_KEY_NAME,
)


def encode_jwt(
    payload: dict,
    private_key_path: Path | str = Path(CERTS_DIR_PATH) / JWT_PRIVATE_KEY_NAME,
    algorithm: str = JWT_ALGORITHM,
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> SecretStr:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    if expire_timedelta:
        expire = now + expire_timedelta

    to_encode = payload.copy()
    to_encode.update(iat=now, exp=expire)

    with open(private_key_path, mode="r") as private_file:
        private_key = private_file.read()

    return SecretStr(
        jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm,
        )
    )
