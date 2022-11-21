from pydantic import BaseModel, Field


class UpdateConfigSchema(BaseModel):
    hide_toxic: bool = Field(..., description="Hide toxic messages")
    hide_unchecked: bool = Field(..., description="Hide unchecked messages")
