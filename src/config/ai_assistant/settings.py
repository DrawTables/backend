import os

from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY: str = os.getenv("OPEN_AI_API_KEY")
OPEN_AI_BASE_URL: str = os.getenv("OPEN_AI_BASE_URL")
PROXY_URL: str = os.getenv("PROXY_URL")

if __name__ == "__main__":
    print(f"{OPEN_AI_API_KEY=}")
    print(f"{OPEN_AI_BASE_URL=}")
