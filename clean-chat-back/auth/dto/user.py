import uuid

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    hide_toxic: bool
    hide_unchecked: bool

    class Config:
        orm_mode = True