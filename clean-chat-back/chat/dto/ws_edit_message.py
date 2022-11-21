import datetime

from pydantic import BaseModel

from chat.dto.message import MessageDTO
from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType


class WebsocketEditMessageDTO(WebsocketMessageBaseDTO):
    type = WebsocketMessageType.UPDATE_MESSAGE
    payload: MessageDTO
