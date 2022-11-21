import uuid

from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType


class WebsocketRemoveUserFromChannelDTO(WebsocketMessageBaseDTO):
    type: WebsocketMessageType.ADD_TO_CHANNEL
    payload: str
