import uuid

from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType


class WebsocketDeletedMessageDTO(WebsocketMessageBaseDTO):
    type = WebsocketMessageType.DELETE_MESSAGE
    payload: str
