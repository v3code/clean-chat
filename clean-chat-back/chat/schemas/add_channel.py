from pydantic import Field, BaseModel


class AddChannelSchema(BaseModel):
    channel_name: str = Field(..., description='name of the channel', max_length=64, min_length=1)