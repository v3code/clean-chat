from chat.dto.message import MessageDTO
from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType, MessageTypeEnum


class WebsocketNewTypeDTO(WebsocketMessageBaseDTO):
    type = WebsocketMessageType.NEW_TYPE
    payload: MessageDTO
