from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.tables.table_position.websocket_manager import ConnectionManager

ROUTER_V1_PREFIX = "/ws/tables-positions"

router_v1 = APIRouter(
    prefix=ROUTER_V1_PREFIX,
    tags=["Users v1"],
)

manager = ConnectionManager()


@router_v1.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int, username: str):
    print(f"{room_id=}")
    await manager.connect(websocket, room_id, user_id)
    await manager.broadcast(f"{username} (ID: {user_id}) присоединился к чату.", room_id, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"{data=}")
            await manager.broadcast(f"{username} (ID: {user_id}): {data}", room_id, user_id)
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast(f"{username} (ID: {user_id}) покинул чат.", room_id, user_id)
