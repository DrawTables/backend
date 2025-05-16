from pydantic import UUID4
from sqlalchemy import or_, not_

from src.core_.specifications import Specification
from src.projects.project.models import Project, ProjectRealtionUser


class ProjectUserHasAccessSpecification(Specification):
    _models_for_join_onclause = [
        {
            "target": ProjectRealtionUser,
            "onclause": ProjectRealtionUser.project_id == Project.project_id,
            "isouter": True,
        }
    ]

    def __init__(self, user_id: UUID4):
        self._filter = or_(
            ProjectRealtionUser.user_id == user_id,
            Project.owner_user_id == user_id,
            not_(Project.private),
        )


class ProjectByOwnerIdSpecification(Specification):
    def __init__(self, user_id: UUID4):
        self._filter = Project.owner_user_id == user_id
