import uuid

from sqlalchemy import select, update, delete, insert, func
from sqlalchemy.orm import joinedload

from chat.enums import MessageTypeEnum
from chat.models.message import MessageModel
from core.common_queries import count_select
from core.singleton import Singleton


class MessageRepository(Singleton):

    def get_message_by_id(self, user_id: uuid.UUID, message_id: uuid.UUID):
        return select(MessageModel).filter(MessageModel.id == message_id, MessageModel.author == user_id)\
            .options(joinedload(MessageModel.author)).execution_options(populate_existing=True)

    def get_messages_by_channel(self, channel_id: uuid.UUID, ):
        return (select(MessageModel).options(joinedload(MessageModel.author))
                .filter(MessageModel.channel_id == channel_id,
                        MessageModel.deleted.is_(False))
                .order_by(MessageModel.created.asc()).execution_options(populate_existing=True)
                )

    def user_has_message(self, user_id: uuid.UUID, message_id: uuid.UUID):
        return count_select(MessageModel).filter(MessageModel.author == user_id, MessageModel.id == message_id)

    def add_message(self, content: str, user_id: uuid.UUID, message_type, channel_id: uuid.UUID):
        return insert(MessageModel).values(content=content, type=message_type, created_by=user_id, channel_id=channel_id)\
            .returning(MessageModel).options(joinedload(MessageModel.author))

    def update_message_type(self, message_id: uuid.UUID, message_type: MessageTypeEnum):
        return update(MessageModel).where(MessageModel.id == message_id).values(type=message_type).returning(MessageModel)

    def edit_message(self, user_id: uuid.UUID, message_id: uuid.UUID, new_content: str):
        return update(MessageModel).where(MessageModel.id == message_id, MessageModel.created_by == user_id)\
            .values(content=new_content, edited=func.now()).returning(MessageModel)\
            .options(joinedload(MessageModel.author))

    def delete_message(self, user_id: uuid.UUID, message_id: uuid.UUID):
        return update(MessageModel).where(MessageModel.id == message_id, MessageModel.created_by == user_id)\
            .values(deleted=True)

    def count_messages_by_channel(self, channel_id: uuid.UUID):
        return count_select(MessageModel).filter(MessageModel.channel_id == channel_id,
                                                 MessageModel.deleted.is_(False))





