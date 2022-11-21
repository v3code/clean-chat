import uuid
from typing import List

from pydantic import BaseModel


class UsersPayload(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        orm_mode = True


class UsersDTO(BaseModel):
    count: int
    payload: List[UsersPayload]
