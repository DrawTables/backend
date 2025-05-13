from pydantic import EmailStr, Field, SecretStr

from src.core_.schemas import RequestModel


class LoginRequest(RequestModel):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)
    password: SecretStr
