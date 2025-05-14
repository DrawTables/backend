from fastapi import WebSocket, WebSocketDisconnect
from pydantic import UUID4

from src.tables.table_position.service import broadcast_tables_coordinates
from src.tables.table_position.websockets_ import ConnectionManager

manager = ConnectionManager()


async def synchronize_tables_positions(
    websocket: WebSocket,
    project_id: UUID4,
    user_id: UUID4,
):
    await manager.connect(websocket, project_id, user_id)
    print(f"Пользователь с ID: [{user_id}] присоединился к чату.")

    try:
        while True:
            await broadcast_tables_coordinates(
                websocket_manager=manager,
                websocket=websocket,
                project_id=project_id,
                user_id=user_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(project_id=project_id, user_id=user_id)
        print(f"Пользователь с ID: [{user_id}] вышел из чата.")
