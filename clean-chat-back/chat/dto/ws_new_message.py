from pydantic import BaseModel

from chat.dto.message import MessageDTO
from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType


class WebsocketNewMessageDTO(WebsocketMessageBaseDTO):
    type = WebsocketMessageType.NEW_MESSAGE
    payload: MessageDTO
