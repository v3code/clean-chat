import uuid

from pydantic import Field, BaseModel


class EditMessageSchema(BaseModel):
    new_content: str = Field(..., description='New content of the message', min_length=1, max_length=2048)