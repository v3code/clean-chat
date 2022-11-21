import uuid

from sqlalchemy import event, Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class UserChannelsModel(Base):
    __tablename__ = "users_to_channels"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False)
