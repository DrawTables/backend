from fastapi import WebSocket
from pydantic import UUID4

from src.tables.table_position.websockets_ import ConnectionManager


async def broadcast_tables_coordinates(
    websocket_manager: ConnectionManager,
    websocket: WebSocket,
    project_id: UUID4,
    user_id: UUID4,
):
    data = await websocket.receive_text()
    await websocket_manager.broadcast(
        project_id=project_id,
        sender_id=user_id,
        data={"message": f"Сообщение: {data}"},
    )
