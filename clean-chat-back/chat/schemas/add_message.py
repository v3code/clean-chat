from pydantic import BaseModel, Field


class AddMessageSchema(BaseModel):
    content: str = Field(..., description='Message content', min_length=1, max_length=2048)