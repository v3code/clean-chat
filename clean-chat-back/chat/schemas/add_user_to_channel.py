import uuid

from pydantic import BaseModel, Field


class AddUserToChannelSchema(BaseModel):
    user_id: uuid.UUID = Field(..., description="Id of the user")
