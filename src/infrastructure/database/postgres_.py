from sqlalchemy.ext.asyncio import create_async_engine

from src.config import POSTGRES_URI

postgres_async_engine = create_async_engine(
    POSTGRES_URI,
    future=True,
    echo=False,
    pool_recycle=60 * 60 * 2,
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=20,
)
