from pydantic import UUID4

from src.exceptions import NotFound


class ApiTokenByIdNotFound(NotFound):
    def __init__(self, api_token_id: UUID4):
        self.DETAIL = f'Токен с id "{api_token_id}" не найден!'
        super().__init__()
