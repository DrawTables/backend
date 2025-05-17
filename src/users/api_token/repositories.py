from src.core_.repository import SQLAlchemyRepository
from src.users.api_token.models import ApiToken


class ApiTokenRepository(SQLAlchemyRepository):
    _model = ApiToken
