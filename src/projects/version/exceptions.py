from pydantic import UUID4

from src.exceptions import NotFound


class VersionByIdNotFound(NotFound):
    def __init__(self, version_id: UUID4):
        self.DETAIL = f'Версия с id "{version_id}" не найден!'
        super().__init__()
