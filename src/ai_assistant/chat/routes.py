from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.auth.tokens.dependencies import is_verified_user, get_current_user
from src.projects.project.dependencies import (
    project_by_id_exists,
    user_have_write_access_to_project,
)
from src.ai_assistant.chat.schemas import (
    ChatMessageRequestSchemas,
    ChatMessageResponseSchemas,
)
from src.ai_assistant.chat.ai_lib import generate_dbml_code
from src.ai_assistant.chat_history import use_cases

ROUTER_V1_PREFIX = "/api/v1/ai-assistant"

ai_assistant_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["AI-Assistant v1"],
    dependencies=[Depends(is_verified_user)],
)


@ai_assistant_router_v1.post(
    "/{project_id}/generate-dbml",
    response_model=ChatMessageResponseSchemas,
    dependencies=[
        Depends(project_by_id_exists),
    ],
)
async def get_ai_assistant(
    project_id: UUID4,
    body: ChatMessageRequestSchemas,
    user: dict = Depends(get_current_user),
):
    await user_have_write_access_to_project(
        project_id=project_id,
        user=user
    )
    response = await generate_dbml_code(body.request)
    await use_cases.create_chat_message(
        project_id=project_id,
        user_message=body.request,
        assistant_message=response,
    )
    return {"response": response}