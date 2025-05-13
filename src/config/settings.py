import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR_PATH = Path(__file__).parent.parent.parent.resolve()
SRC_DIR_PATH = PROJECT_DIR_PATH / "src"

load_dotenv()
BACKEND_API_PORT: int = int(os.getenv("BACKEND_API_PORT"))


if __name__ == "__main__":
    print(f"{PROJECT_DIR_PATH=}")
    print(f"{SRC_DIR_PATH=}\n")
    print(f"{BACKEND_API_PORT=}")
