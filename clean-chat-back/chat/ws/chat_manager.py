import asyncio
import uuid
from typing import Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from core.singleton import Singleton


class ChatWebsocketManager(Singleton):
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.active_users: Dict[str, WebSocket] = {}

    def register_connection(self, websocket: WebSocket, channel_id: uuid.UUID, user_id: uuid.UUID):
        channel_id = str(channel_id)
        user_id = str(user_id)
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = {}
        self.active_connections[channel_id][user_id] = websocket
        if user_id not in self.active_users:
            self.active_users[user_id] = {}
        self.active_users[user_id] = websocket

    def disconnect(self, channel_id: uuid.UUID, user_id: uuid.UUID):
        channel_id = str(channel_id)
        user_id = str(user_id)
        del self.active_connections[channel_id][user_id]
        del self.active_users[user_id]

    async def send_to_user(self, user_id: uuid.UUID, message: BaseModel):
        user_id = str(user_id)
        if user_id not in self.active_users:
            return
        return await self.active_users[user_id].send_json(message.dict())

    async def broadcast(self, channel_id: uuid.UUID, message: Any):
        channel_id = str(channel_id)
        if channel_id not in self.active_connections:
            return
        tasks = []
        for connection in self.active_connections[channel_id].values():
            tasks.append(connection.send_json(message))
        await asyncio.gather(*tasks)

    async def process_loop(self, websocket: WebSocket, user_id: uuid.UUID, channel_id: uuid.UUID):
        self.register_connection(websocket, channel_id, user_id)
        try:
            while True:
                await websocket.receive_json()
        except WebSocketDisconnect:
            self.disconnect(channel_id, user_id)


