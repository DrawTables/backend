from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import UUID4

from src.tables.table_position.websockets_ import ConnectionManager

ROUTER_V1_PREFIX = "/ws/v1/tables-positions"

router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Users v1"],
)

manager = ConnectionManager()


@router_v1.websocket("/{project_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: UUID4,
    user_id: UUID4,
):
    await manager.connect(websocket, project_id, user_id)
    await manager.broadcast(
        project_id=project_id,
        sender_id=user_id,
        data={"message": f"Пользователь с ID: [{user_id}] присоединился к чату."},
    )

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(
                project_id=project_id,
                sender_id=user_id,
                data={"message": f"Сообщение: {data}"},
            )

    except WebSocketDisconnect:
        manager.disconnect(project_id=project_id, user_id=user_id)
        await manager.broadcast(
            project_id=project_id,
            sender_id=user_id,
            data={"message": f"Пользователь с ID: [{user_id}] покинул чат."},
        )
