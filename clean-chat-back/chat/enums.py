import enum


class MessageTypeEnum(str, enum.Enum):
    UNCHECKED = 'UNCHECKED'
    TOXIC = 'TOXIC'
    SAFE = 'SAFE'


class WebsocketMessageType(str, enum.Enum):
    NEW_TYPE = 'new_type'
    NEW_MESSAGE = 'new_message'
    UPDATE_MESSAGE = 'update_message'
    DELETE_MESSAGE = 'delete_message'
    ADD_TO_CHANNEL = 'add_to_channel'
    REMOVE_FROM_CHANNEL = 'remove_from_channel'