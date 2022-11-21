import uuid

from chat.models.channel import ChannelModel
from chat.repos.channel import ChannelRepository
from chat.services.chat_ws import ChatWebsocketService
from core.singleton import Singleton
from database import db


class ChannelService(Singleton):

    def __init__(self):
        self._channel_repository = ChannelRepository()

    async def create_channel(self, user_id: uuid.UUID, channel_name: str):
        async with db.transaction():
            channel = await db.fetch_one(self._channel_repository.add_channel(channel_name).returning(ChannelModel))
            await db.execute(self._channel_repository.add_user_to_channel(user_id=user_id, channel_id=channel.id))
        return channel
        # await self._ws.add_user_to_channel(user_id, channel_id)
    def get_by_id(self, id: uuid.UUID):
        return db.fetch_one(self._channel_repository.get_by_id(id))

    async def get_user_channels(self, user_id: uuid.UUID):
        count = await db.fetch_one(self._channel_repository.count_user_channels(user_id))
        channels = await db.fetch_all(self._channel_repository.get_channels(user_id))
        return channels, count[0]

    def get_user_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        return db.fetch_one(self._channel_repository.get_user_channel(user_id, channel_id))

    async def user_has_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        count = await db.fetch_one(self._channel_repository.user_has_channel(user_id, channel_id))
        return bool(count[0])

    async def add_user_to_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        user_channel = await self.get_user_channel(user_id, channel_id)
        if not user_channel:
            await db.execute(self._channel_repository.add_user_to_channel(user_id, channel_id))
        return user_channel
            # await self._ws.add_user_to_channel(user_id, channel=user_channel)

    async def remove_user_from_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        user_channel = await self.get_user_channel(user_id, channel_id)
        if user_channel:
            await db.execute(self._channel_repository.add_user_to_channel(user_id, channel_id))
        return user_channel
            # await self._ws.remove_user_from_channel(user_id, channel_id=user_channel.id)
