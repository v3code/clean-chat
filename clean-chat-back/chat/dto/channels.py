from typing import List

from pydantic import BaseModel

from chat.dto.channel import ChannelDTO


class ChannelsDTO(BaseModel):
    count: int
    payload: List[ChannelDTO]
