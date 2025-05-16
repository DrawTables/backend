from src.core_.repository import SQLAlchemyRepository
from src.projects.version.models import Version


class VersionRepository(SQLAlchemyRepository):
    _model = Version
