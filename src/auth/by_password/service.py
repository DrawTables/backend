import bcrypt
from pydantic import SecretBytes, SecretStr


def get_hashed_password(plain_password: SecretStr) -> SecretBytes:
    return SecretBytes(
        bcrypt.hashpw(
            plain_password.get_secret_value().encode(),
            bcrypt.gensalt(),
        )
    )


def is_valid_password(
    plain_password: SecretStr,
    hashed_password: SecretBytes,
) -> bool:
    return bcrypt.checkpw(
        password=plain_password.get_secret_value().encode(),
        hashed_password=hashed_password.get_secret_value(),
    )


if __name__ == "__main__":
    plain_password_ = SecretStr("password")
    hashed_password_ = get_hashed_password(plain_password_)

    validation_result = is_valid_password(plain_password_, hashed_password_)
    print(validation_result)
