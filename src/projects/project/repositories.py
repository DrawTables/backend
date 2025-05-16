from src.core_.repository import SQLAlchemyRepository
from src.projects.project.models import Project, ProjectRealtionUser


class ProjectRepository(SQLAlchemyRepository):
    _model = Project


class ProjectRealtionUserRepository(SQLAlchemyRepository):
    _model = ProjectRealtionUser
