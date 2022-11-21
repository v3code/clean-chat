import asyncio
import functools
import uuid

from chat.enums import MessageTypeEnum
from main import celery
from detoxify import Detoxify


model = Detoxify('original')
# def sync(f):
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
#     return wrapper

def check_message(content: str):
    results = model.predict(content)
    message_type = MessageTypeEnum.TOXIC if results['toxicity'] > 0.5 else MessageTypeEnum.SAFE
    return message_type

# @celery.task
# def check_message(message_id: uuid.UUID, content: str):
#     # results = model.predict(content)
#     # message_type = MessageTypeEnum.TOXIC if results['toxicity'] > 0.5 else MessageTypeEnum.SAFE
#     message_type = MessageTypeEnum.TOXIC
#     return {"message_id": message_id, "message_type": message_type}
