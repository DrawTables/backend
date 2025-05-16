from src.projects.project.router import projects_router_v1
from src.projects.version.routes import versions_router_v1

projects_routers_v1 = [
    versions_router_v1,
    projects_router_v1,
]
