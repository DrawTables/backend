from fastapi import APIRouter, WebSocket
from pydantic import UUID4

from src.tables.table_position.use_cases import synchronize_tables_positions

ROUTER_V1_PREFIX = "/ws/v1/tables-positions"

router_v1 = APIRouter(prefix=ROUTER_V1_PREFIX)


@router_v1.websocket("/{project_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: UUID4,
    user_id: UUID4,
):
    await synchronize_tables_positions(
        websocket=websocket,
        project_id=project_id,
        user_id=user_id,
    )
