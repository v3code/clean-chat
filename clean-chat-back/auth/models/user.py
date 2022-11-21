import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, event, text
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, server_default=text("uuid_generate_v4()"))
    username = Column(String(length=64), index=True, nullable=False, unique=True)
    email = Column(String(length=320), index=True, nullable=False, unique=True)
    password = Column(String(length=76), index=True, nullable=False, unique=True)
    hide_toxic = Column(Boolean, server_default=text("TRUE"))
    hide_unchecked = Column(Boolean, server_default=text("TRUE"))
    deleted = Column(Boolean, server_default=text("FALSE"))
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


@event.listens_for(UserModel, 'before_update')
def receive_after_update(mapper, connection, target):
    target.updated = func.now()
