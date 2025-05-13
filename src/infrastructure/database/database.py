from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from src.core_.schemas import SchemaModel
from src.infrastructure.database.postgres_ import postgres_async_engine

async_session_maker = async_sessionmaker(
    bind=postgres_async_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# TODO: Почитать подробней! Для чего используются "AsyncAttrs" и "eager_defaults"?
class Base(AsyncAttrs, DeclarativeBase):
    id: None
    # refresh server defaults with asyncio
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_schema(self) -> SchemaModel:
        raise NotImplementedError
