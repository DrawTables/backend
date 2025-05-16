from fastapi import APIRouter, Depends

from src.auth.tokens.dependencies import is_verified_user
from src.ai_assistant.schemas import (
    ChatMessageRequestSchemas,
    ChatMessageResponseSchemas,
)
from src.ai_assistant.ai_lib import generate_dbml_code

ROUTER_V1_PREFIX = "/api/v1/ai-assistant"

ai_assistant_router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["AI-Assistant v1"],
    dependencies=[Depends(is_verified_user)],
)


@ai_assistant_router_v1.post(
    "/",
    response_model=ChatMessageResponseSchemas,
)
async def get_ai_assistant(
    body: ChatMessageRequestSchemas,
):
    response = generate_dbml_code(body.request)
    return {"response": response}