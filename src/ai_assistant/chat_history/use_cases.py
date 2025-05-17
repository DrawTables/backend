from pydantic import UUID4

from src.ai_assistant.chat_history.schemas import AssistantChatMessageResponseSchema
from src.core_.pagination.schemas import PaginationParams
from src.core_.work_unit import UnitOfWork


async def get_chat_history(
    project_id: UUID4,
    pagination: PaginationParams,
) -> tuple[int, list[AssistantChatMessageResponseSchema]]:
    uow = UnitOfWork()
    async with uow:
        chat_history = await uow.assistant_chat_messages.get_by_filters(
            filter_by={
                "project_id": project_id,
            },
            pagination=pagination,
        )
        amount = await uow.assistant_chat_messages.amount(
            **{
                "project_id": project_id,
            },
        )
    return amount, chat_history


async def delete_chat_history(
    project_id: UUID4,
) -> None:
    uow = UnitOfWork()
    async with uow:
        await uow.assistant_chat_messages.delete_by_filters(
            filter_by={
                "project_id": project_id,
            },
        )
        await uow.commit()


async def create_chat_message(
    project_id: UUID4,
    user_message: str,
    assistant_message: str,
) -> AssistantChatMessageResponseSchema:
    uow = UnitOfWork()
    async with uow:
        chat_message = await uow.assistant_chat_messages.create(
            data={
                "project_id": project_id,
                "user_message": user_message,
                "assistant_message": assistant_message,
            },
        )
        await uow.commit()
    return chat_message
