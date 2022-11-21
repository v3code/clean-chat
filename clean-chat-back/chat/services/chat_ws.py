import uuid

from chat.dto.channel import ChannelDTO
from chat.dto.message import MessageDTO
from chat.dto.ws_add_user_to_channel import WebsocketAddUserToChannelDTO
from chat.dto.ws_base import WebsocketMessageBaseDTO
from chat.dto.ws_deleted_message import WebsocketDeletedMessageDTO
from chat.dto.ws_edit_message import WebsocketEditMessageDTO
from chat.dto.ws_new_message import WebsocketNewMessageDTO
from chat.dto.ws_new_type import WebsocketNewTypeDTO
from chat.models.channel import ChannelModel
from chat.models.message import MessageModel
from chat.ws.chat_manager import ChatWebsocketManager
from core.singleton import Singleton


class ChatWebsocketService(Singleton):

    def __init__(self):
        self._chat_ws_manager = ChatWebsocketManager()

    def send_to_channel(self, payload: WebsocketMessageBaseDTO, channel_id: uuid.UUID):
        return self._chat_ws_manager.broadcast(channel_id, payload.dict())

    def add_user_to_channel(self, user_id: uuid.UUID, channel: ChannelModel):
        ws_message_payload = WebsocketAddUserToChannelDTO(payload=ChannelDTO.from_orm(channel))
        return self._chat_ws_manager.send_to_user(user_id, ws_message_payload)

    def remove_user_from_channel(self, user_id: uuid.UUID, channel_id: uuid.UUID):
        ws_message_payload = WebsocketAddUserToChannelDTO(payload=channel_id)
        return self._chat_ws_manager.send_to_user(user_id, ws_message_payload)

    def send_new_message(self, message: MessageModel):
        ws_message_payload = MessageDTO.from_orm(message)
        ws_message_payload.id = str(ws_message_payload.id)  # TODO FIX THIS, JSON ENCODER CAN'T SERIALIZE ANYTHING
        ws_message_payload.author.id = str(ws_message_payload.author.id)
        ws_message_payload.edited = str(ws_message_payload.edited)
        ws_message_payload.created = str(ws_message_payload.created)
        return self.send_to_channel(payload=WebsocketNewMessageDTO(payload=ws_message_payload),
                                    channel_id=message.channel_id)

    def send_new_message_type(self, message: MessageModel):
        ws_message_payload = MessageDTO.from_orm(message)
        ws_message_payload.id = str(ws_message_payload.id)  # TODO FIX THIS, JSON ENCODER CAN'T SERIALIZE ANYTHING
        ws_message_payload.author.id = str(ws_message_payload.author.id)
        ws_message_payload.edited = str(ws_message_payload.edited)
        ws_message_payload.created = str(ws_message_payload.created)
        return self.send_to_channel(payload=WebsocketNewTypeDTO(payload=ws_message_payload),
                                    channel_id=message.channel_id)

    def send_edited_message(self, message: MessageModel):
        ws_message_payload = MessageDTO.from_orm(message)
        ws_message_payload.id = str(ws_message_payload.id)  # TODO FIX THIS, JSON ENCODER CAN'T SERIALIZE ANYTHING
        ws_message_payload.author.id = str(ws_message_payload.author.id)
        ws_message_payload.edited = str(ws_message_payload.edited)
        ws_message_payload.created = str(ws_message_payload.created)
        return self.send_to_channel(payload=WebsocketEditMessageDTO(payload=ws_message_payload),
                                    channel_id=message.channel_id)

    def send_deleted_message(self, message_id: uuid.UUID, channel_id: uuid.UUID):
        return self.send_to_channel(payload=WebsocketDeletedMessageDTO(payload=str(message_id)),
                                    channel_id=channel_id)
