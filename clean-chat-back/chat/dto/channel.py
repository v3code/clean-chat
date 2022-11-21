import uuid

from pydantic import BaseModel


class ChannelDTO(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True
