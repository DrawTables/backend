from src.core_.repository import SQLAlchemyRepository
from src.projects.project.models import Project


class ProjectRepository(SQLAlchemyRepository):
    _model = Project
