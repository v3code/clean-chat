from pydantic import BaseModel

from auth.dto.user import UserDTO


class LoginDTO(BaseModel):
    token: str
    user: UserDTO
