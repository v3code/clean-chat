import datetime
import uuid

from pydantic import BaseModel

from chat.enums import MessageTypeEnum


class Author(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        orm_mode = True

class MessageDTO(BaseModel):
    id: uuid.UUID
    content: str
    created: datetime.datetime
    edited: datetime.datetime
    type: MessageTypeEnum
    author: Author

    class Config:
        orm_mode = True

