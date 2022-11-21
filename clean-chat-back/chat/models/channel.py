import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, event, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class ChannelModel(Base):
    __tablename__ = "channels"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, index=True, nullable=False)
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    archived = Column(Boolean, server_default=text("FALSE"))

@event.listens_for(ChannelModel, 'before_update')
def receive_after_update(mapper, connection, target):
    target.updated = func.now()




