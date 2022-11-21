import uuid

from chat.dto.channel import ChannelDTO
from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.enums import WebsocketMessageType


class WebsocketAddUserToChannelDTO(WebsocketMessageBaseDTO):
    type = WebsocketMessageType.ADD_TO_CHANNEL
    payload: ChannelDTO

