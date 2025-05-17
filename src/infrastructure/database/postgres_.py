from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import POSTGRES_URI, get_sandbox_postgres_uri

postgres_async_engine = create_async_engine(
    POSTGRES_URI,
    future=True,
    echo=False,
    pool_recycle=60 * 60 * 2,
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=20,
)

async def create_sandbox_postgres_async_engine(database_name: str) -> AsyncSession:
    sandbox_postgres_uri = get_sandbox_postgres_uri(database_name)
    return create_async_engine(
        sandbox_postgres_uri,
        future=True,
        echo=False,
        pool_recycle=60 * 60 * 2,
        pool_pre_ping=True,
        pool_size=50,
        max_overflow=20,
    )