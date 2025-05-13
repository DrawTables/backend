from src.core_.repository import SQLAlchemyRepository
from src.users.user.models import User


class UserRepository(SQLAlchemyRepository):
    _model = User
