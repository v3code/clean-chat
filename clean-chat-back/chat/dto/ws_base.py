from typing import Any

from pydantic import BaseModel

from chat.enums import WebsocketMessageType


class WebsocketMessageBaseDTO(BaseModel):
    type: WebsocketMessageType
    payload: Any
