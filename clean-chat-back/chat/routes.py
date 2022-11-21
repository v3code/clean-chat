import uuid
import jwt
from starlette.requests import Request

from auth.guard.jwt import verify_jwt
from auth.services.token import TokenService
from auth.services.user import UserService
from chat.dto.channel import ChannelDTO
from chat.dto.channels import ChannelsDTO
from chat.dto.message import MessageDTO, Author
from chat.dto.messages import MessagesDTO
from chat.schemas.add_channel import AddChannelSchema
from chat.schemas.add_message import AddMessageSchema
from chat.schemas.add_user_to_channel import AddUserToChannelSchema
from chat.schemas.edit_message import EditMessageSchema
from chat.services.channel import ChannelService
from chat.services.chat_ws import ChatWebsocketService
from chat.services.message import MessageService
from fastapi import WebSocket, Depends, Body, HTTPException

from chat.ws.chat_manager import ChatWebsocketManager
from main import app, GLOBAL_ROUTE
from ml.tasks import check_message
from utils import create_subrouter

messages_service = MessageService()
channel_service = ChannelService()
chat_ws_service = ChatWebsocketService()
chat_ws_manager = ChatWebsocketManager()
token_service = TokenService()
user_service = UserService()

SUBROUTE = '/chat'

subrouter = create_subrouter(f'{GLOBAL_ROUTE}{SUBROUTE}')


@app.get(subrouter('/channel/{channel_id}/message'), dependencies=[Depends(verify_jwt)])
async def get_all_messages(request: Request, channel_id: uuid.UUID, skip: int = 0, limit: int = 10):
    user_id = request.state.user_id
    messages, total_count = await messages_service.get_messages_by_channel(user_id, channel_id)
    # TODO change orm because async sqlalchemy sucks
    for message in messages:
        message.author = await user_service.get_by_id(message.created_by)
    return MessagesDTO(count=total_count, payload=list(map(MessageDTO.from_orm, messages)))


@app.post(subrouter('/channel/{channel_id}/message'), dependencies=[Depends(verify_jwt)], status_code=201)
async def add_message(request: Request, channel_id: uuid.UUID, message: AddMessageSchema):
    user_id = request.state.user_id
    message = await messages_service.add_message(user_id=user_id, channel_id=channel_id, **message.dict())
    message.author = await user_service.get_by_id(user_id)
    await chat_ws_service.send_new_message(message)
    return MessageDTO.from_orm(message)

# @app.patch(subrouter('/channel/{channel_id}/message'), dependencies=[Depends(verify_jwt)], status_code=201)
# async def add_message(request: Request, channel_id: uuid.UUID, message: AddMessageSchema):
#     user_id = request.state.user_id
#     message = await messages_service.add_message(user_id=user_id, channel_id=channel_id, **message.dict())
#     await chat_ws_service.send_new_message(message)
#     return MessageDTO.from_orm(message)

@app.patch(subrouter('/channel/{channel_id}/message/{message_id}'), dependencies=[Depends(verify_jwt)])
async def edit_message(request: Request, channel_id: uuid.UUID, message_id: uuid.UUID, message: EditMessageSchema):
    user_id = request.state.user_id
    message = await messages_service.edit_message(user_id=user_id, message_id=message_id, **message.dict())
    message.author = await user_service.get_by_id(user_id)
    await chat_ws_service.send_edited_message(message)
    return MessageDTO.from_orm(message)


@app.delete(subrouter('/channel/{channel_id}/message/{message_id}'), dependencies=[Depends(verify_jwt)])
async def delete_message(request: Request, channel_id: uuid.UUID, message_id: uuid.UUID):
    user_id = request.state.user_id
    message = await messages_service.delete_message(user_id, message_id)
    await chat_ws_service.send_deleted_message(message_id, channel_id)
    return "Success"

# @app.put(subrouter('/channel/{channel_id}/user'), dependencies=[Depends(verify_jwt)])
# async def add_user_to_channel(request: Request, channel_id: uuid.UUID, body: AddUserToChannelSchema = Body()):
#     user_id = request.state.user_id
#     if not await channel_service.user_has_channel(user_id=user_id, channel_id=channel_id):
#         raise HTTPException(status_code=401, detail='Only users that already in this channel can add other')
#     user_channel = await channel_service.add_user_to_channel(channel_id=channel_id, **body.dict())
#     if user_channel is None:
#         channel = await channel_service.get_by_id(channel_id)
#         await chat_ws_service.add_user_to_channel(**body.dict(), channel=channel)
#     return 'Success'

@app.get(subrouter('/channel'), dependencies=[Depends(verify_jwt)])
async def get_all_channels(request: Request, skip: int = 0, limit: int = 10):
    user_id = request.state.user_id
    channels, total_count = await channel_service.get_user_channels(user_id)
    return ChannelsDTO(count=total_count, payload=list(map(ChannelDTO.from_orm, channels)))


# @app.post(subrouter('/channel'), dependencies=[Depends(verify_jwt)])
# async def create_channel(request: Request, channel_data: AddChannelSchema = Body()):
#     user_id = request.state.user_id
#     channel = await channel_service.create_channel(user_id=user_id, **channel_data.dict())
#     return ChannelDTO.from_orm(channel)


@app.websocket(subrouter('/ws/{channel_id}'))
async def receive_connection(ws: WebSocket, channel_id: uuid.UUID, token: str):
    await ws.accept()
    decoded, is_error, reason = token_service.check_jwt(token)
    if is_error:
        await ws.close(1008, reason)
        return
    user_id = decoded['user_id']
    await chat_ws_manager.process_loop(ws, user_id, channel_id)
