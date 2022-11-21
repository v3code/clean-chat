import uuid

from sqlalchemy import select, insert, update, delete

from chat.models.channel import ChannelModel
from chat.models.user_channels import UserChannelsModel
from core.common_queries import count_select
from core.singleton import Singleton


class ChannelRepository(Singleton):

    def get_user_channels(self, user_id: uuid.UUID):
        return select(UserChannelsModel.channel_id).filter(UserChannelsModel.user_id == user_id)

    def count_user_channels(self, user_id: uuid.UUID):
        return count_select(ChannelModel)

    def get_channels(self, user_id: uuid.UUID, skip=0, limit=10):
        return select(ChannelModel)

    def get_by_id(self, id: uuid.UUID):
        return select(ChannelModel).filter(ChannelModel.id == id)

    def archive_channel(self, channel_id: uuid.UUID):
        return update(ChannelModel).where(channel_id == channel_id).values(archived=True)

    def add_channel(self, channel_name: str):
        return insert(ChannelModel).values(name=channel_name)

    def get_user_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        return select(UserChannelsModel).filter(UserChannelsModel.user_id == user_id,
                                                UserChannelsModel.channel_id == channel_id)

    def user_has_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        return count_select(UserChannelsModel).filter(UserChannelsModel.user_id == user_id,
                                                      UserChannelsModel.channel_id == channel_id)

    def add_user_to_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        return insert(UserChannelsModel).values(user_id=user_id, channel_id=channel_id)

    def delete_user_from_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        return delete(UserChannelsModel).where(UserChannelsModel.user_id == user_id,
                                               UserChannelsModel.channel_id == channel_id)
