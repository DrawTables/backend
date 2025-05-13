from collections.abc import AsyncGenerator

from redis.asyncio import from_url, Redis

from src.config.redis import settings


async def get_redis_session() -> AsyncGenerator[Redis]:
    session = from_url(
        settings.REDIS_URI,
        encoding="utf-8",
        decode_responses=True,
    )
    print(f"Redis get new session: {await session.ping()}")
    yield session
    await session.close()
