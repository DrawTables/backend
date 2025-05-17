import sys
from pathlib import Path

PROJECT_DIR_PATH = Path(__file__).parent.parent
sys.path.append(str(PROJECT_DIR_PATH))

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.auth.by_password.router import router_v1 as auth_by_login_router_v1
from src.auth.tokens.router import router_v1 as tokens_router_v1
from src.config import settings
from src.users.user.router import router_v1 as users_router_v1
from src.projects.projects_routes import projects_routers_v1
from src.ai_assistant.routes import ai_assistant_router_v1
from src.users.api_token.routes import api_tokens_router_v1

app = FastAPI()

docs_router = APIRouter(prefix="/api/docs")
SWAGGER_UI_HTML = get_swagger_ui_html(
    openapi_url="/api/docs/openapi.json",
    title="docs",
)


@docs_router.get("", include_in_schema=False)
async def get_documentation():
    return SWAGGER_UI_HTML


@docs_router.get("/openapi.json", include_in_schema=False)
async def openapi(request: Request):
    return get_openapi(
        title="DrawTables API",
        version="0.1.0",
        routes=request.app.routes,
    )


origins = [
    "http://localhost:3055",
    "http://localhost:5173",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs_router)

app.include_router(auth_by_login_router_v1)
app.include_router(tokens_router_v1)
app.include_router(users_router_v1)
app.include_router(ai_assistant_router_v1)
app.include_router(api_tokens_router_v1)

for router in projects_routers_v1:
    app.include_router(router)
    
if __name__ == "__main__":
    uvicorn.run(
        "src.__main__:app",
        host="0.0.0.0",
        port=settings.BACKEND_API_PORT,
        log_level="info",
        reload=True,
        workers=4,
    )
