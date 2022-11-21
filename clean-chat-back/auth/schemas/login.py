from pydantic import BaseModel, Field, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description='Email address')
    password: str = Field(..., description='Password', min_length=8, max_length=64)
