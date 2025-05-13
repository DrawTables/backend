from datetime import datetime
from typing import Any

from pydantic import EmailStr, Field, SecretBytes, SecretStr, UUID4

from src.core_.schemas import SchemaModel, RequestModel, ResponseModel


class UserSchema(SchemaModel):
    user_id: UUID4
    email: EmailStr | None
    username: str | None

    hashed_password: SecretBytes

    created_at: datetime
    updated_at: datetime


class UserResponse(UserSchema, ResponseModel):
    hashed_password: Any = Field(exclude=True)


class UserCreateRequest(RequestModel):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)
    password: SecretStr


class UserUpdateRequest(RequestModel):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)
