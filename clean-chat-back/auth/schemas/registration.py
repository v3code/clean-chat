from pydantic import Field

from auth.schemas.login import LoginSchema


class RegistrationSchema(LoginSchema):
    username: str = Field(..., description='Username', min_length=4, max_length=124)
