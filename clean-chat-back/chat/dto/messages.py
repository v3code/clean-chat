from typing import List

from pydantic import BaseModel

from chat.dto.message import MessageDTO


class MessagesDTO(BaseModel):
    count: int
    payload: List[MessageDTO]
