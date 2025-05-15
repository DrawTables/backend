from pydantic import UUID4

from src.exceptions import NotFound


class ProjectByIdNotFound(NotFound):
    def __init__(self, project_id: UUID4):
        self.DETAIL = f'Проект с id "{project_id}" не найден!'
        super().__init__()
