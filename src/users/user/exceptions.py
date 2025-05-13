from pydantic import EmailStr, UUID4

from src.exceptions import AlreadyExists, NotFound


class UserByIdNotFound(NotFound):
    def __init__(self, user_id: UUID4):
        self.DETAIL = f'Пользователь с id "{user_id}" не найден!'
        super().__init__()


class UserByEmailAlreadyExists(AlreadyExists):
    def __init__(self, email: EmailStr):
        self.DETAIL = f'Пользователь с почтой "{email}" уже существует!'
        super().__init__()


class UserByUsernameAlreadyExists(AlreadyExists):
    def __init__(self, username: str):
        self.DETAIL = f'Пользователь с именем "{username}" уже существует!'
        super().__init__()


class UserByEmailNotFound(NotFound):
    def __init__(self, email: EmailStr):
        self.DETAIL = f'Пользователь с почтой "{email}" не существует!'
        super().__init__()


class UserByUsernameNotFound(NotFound):
    def __init__(self, username: str):
        self.DETAIL = f'Пользователя с именем "{username}" не существует!'
        super().__init__()
