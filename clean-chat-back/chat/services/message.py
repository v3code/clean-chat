import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from auth.services.user import UserService
from chat.enums import MessageTypeEnum
from chat.repos.message import MessageRepository
from chat.services.chat_ws import ChatWebsocketService
from core.singleton import Singleton
from database import db
from ml.tasks import check_message


class MessageService(Singleton):
    def __init__(self):
        self._messageRepository = MessageRepository()
        self._chat_ws_service = ChatWebsocketService()
        self._user_service = UserService()

    async def user_has_message(self, user_id: uuid.UUID, message_id: uuid.UUID):
        count = await db.fetch_one(self._messageRepository.user_has_message(user_id, message_id))
        return count[0] > 0

    async def handle_message_type_result(self, message_id: uuid.UUID, message_type: MessageTypeEnum):
        message = await self.update_type(message_id, message_type)
        message.author = await self._user_service.get_by_id(message.created_by)
        await self._chat_ws_service.send_new_message_type(message)

    async def get_messages_by_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        total_count = await db.fetch_one(self._messageRepository.count_messages_by_channel(channel_id))
        result = await db.fetch_all(self._messageRepository.get_messages_by_channel(channel_id))
        return result, total_count[0]

    def update_type(self, message_id: uuid.UUID, message_type: MessageTypeEnum):
        return db.fetch_one(self._messageRepository.update_message_type(message_id, message_type))

    def delete_message(self, user_id: uuid.UUID, message_id: uuid.UUID):
        return db.fetch_one(self._messageRepository.delete_message(user_id, message_id))

    def edit_message(self, user_id: uuid.UUID, message_id: uuid.UUID, new_content: str):
        return db.fetch_one(self._messageRepository.edit_message(user_id, message_id, new_content))

    def add_message(self, user_id: uuid.UUID, channel_id: uuid.UUID, content: str):
        message_type = check_message(content)
        return db.fetch_one(self._messageRepository.add_message(user_id=user_id, message_type=message_type,
                                                                content=content, channel_id=channel_id))
