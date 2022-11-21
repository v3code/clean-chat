import uuid

from sqlalchemy import Column, String, event, DateTime, func, Boolean, Enum, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from chat.enums import MessageTypeEnum
from database import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, server_default=text("uuid_generate_v4()"))
    content = Column(String, index=True, nullable=False)
    deleted = Column(Boolean, server_default=text("FALSE"))
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    edited = Column(DateTime, nullable=True)
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    type = Column(Enum(MessageTypeEnum), server_default="UNCHECKED")
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    author = relationship("UserModel", lazy='joined', innerjoin=True)




@event.listens_for(MessageModel, 'before_update')
def receive_after_update(mapper, connection, target):
    target.updated = func.now()
