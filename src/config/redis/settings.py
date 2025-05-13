import os

from dotenv import load_dotenv

load_dotenv()
REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = int(os.getenv("REDIS_PORT"))
REDIS_PASS: str = os.getenv("REDIS_PASS")

REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}"


if __name__ == "__main__":
    print(f"{REDIS_HOST=}")
    print(f"{REDIS_PORT=}")
