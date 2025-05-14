from typing import Dict

from fastapi import WebSocket
from pydantic import UUID4


class ConnectionManager:
    def __init__(self):
        # Хранение активных соединений в виде {room_id: {user_id: WebSocket}}
        self.active_connections: Dict[UUID4, Dict[UUID4, WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        project_id: UUID4,
        user_id: UUID4,
    ):
        """
        Устанавливает соединение с пользователем.
        websocket.accept() — подтверждает подключение.
        """
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = {}

        self.active_connections[project_id][user_id] = websocket

    def disconnect(
        self,
        project_id: UUID4,
        user_id: UUID4,
    ):
        """
        Закрывает соединение и удаляет его из списка активных подключений.
        Если в комнате больше нет пользователей, удаляет комнату.
        """
        if (
            project_id in self.active_connections
            and user_id in self.active_connections[project_id]
        ):
            del self.active_connections[project_id][user_id]
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def broadcast(
        self,
        project_id: UUID4,
        sender_id: UUID4,
        data: dict,
    ):
        """
        Рассылает сообщение всем пользователям в комнате.
        """
        if project_id in self.active_connections:
            for user_id, connection in self.active_connections[project_id].items():
                message_with_class = {
                    "is_self": user_id == sender_id,
                    "data": data,
                }
                await connection.send_json(message_with_class)
