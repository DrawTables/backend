import os

from dotenv import load_dotenv

load_dotenv()
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASS: str = os.getenv("POSTGRES_PASS")
POSTGRES_BASE: str = os.getenv("POSTGRES_BASE")

POSTGRES_URI = (
    "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_BASE,
    )
)


if __name__ == "__main__":
    print(f"{POSTGRES_HOST=}")
    print(f"{POSTGRES_PORT=}")
    print(f"{POSTGRES_USER=}")
    print(f"{POSTGRES_BASE=}")
