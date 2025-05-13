from pathlib import Path

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from pydantic import SecretBytes, SecretStr
from src.config.security.settings import (
    CERTS_DIR_PATH,
    JWT_ALGORITHM,
    JWT_PUBLIC_KEY_NAME,
)

from src.exceptions import NotAuthenticated


def decode_jwt(
    token: SecretStr | SecretBytes,
    public_key_path: Path | str = Path(CERTS_DIR_PATH) / JWT_PUBLIC_KEY_NAME,
    algorithm: str = JWT_ALGORITHM,
):
    with open(public_key_path) as public_file:
        public_key = public_file.read()

    try:
        decoded_data = jwt.decode(
            jwt=token.get_secret_value(),
            key=public_key,
            algorithms=[algorithm],
        )
        return decoded_data

    except DecodeError as error:
        # TODO: Подумать про логирование
        print(f"DecodeError: {error}")
        return

    except ExpiredSignatureError as error:
        print(f"Error: {error}")
        raise NotAuthenticated
