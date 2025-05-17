from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from src.ai_assistant.chat_history import use_cases
from src.ai_assistant.chat_history.schemas import AssistantChatMessageResponseSchema
from src.auth.tokens.dependencies import get_current_user, is_verified_user
from src.core_.pagination.dependencies import PaginationParamsDependency
from src.core_.pagination.schemas import PaginationResponse
from src.projects.project.dependencies import (
    project_by_id_exists,
    user_have_read_access_to_project,
    user_have_write_access_to_project,
)

ROUTER_V1_PREFIX = "/api/v1/ai-assistant/chat-history"

chat_history_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Ai-Assistant Chat History v1"],
    dependencies=[Depends(is_verified_user)],
)


@chat_history_router_v1.get(
    "/{project_id}/messages",
    response_model=PaginationResponse[AssistantChatMessageResponseSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(project_by_id_exists),
    ],
)
async def get_chat_history(
    project_id: UUID4,
    pagination: PaginationParamsDependency,
    user: dict = Depends(get_current_user),
):
    await user_have_read_access_to_project(project_id=project_id, user=user)
    amount, chat_history = await use_cases.get_chat_history(
        project_id=project_id,
        pagination=pagination,
    )
    return {
        "entities": chat_history,
        "entities_amount": amount,
    }


@chat_history_router_v1.delete(
    "/{project_id}/messages/",
    response_model=AssistantChatMessageResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(project_by_id_exists),
    ],
)
async def delete_chat_history(
    project_id: UUID4,
    user: dict = Depends(get_current_user),
):
    await user_have_write_access_to_project(project_id=project_id, user=user)
    await use_cases.delete_chat_history(
        project_id=project_id,
    )
