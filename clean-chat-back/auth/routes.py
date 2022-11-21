from fastapi import Depends, HTTPException, Body
from starlette.requests import Request

from auth.dto.login import LoginDTO
from auth.dto.user import UserDTO
from auth.dto.users import UsersDTO, UsersPayload
from auth.guard.jwt import verify_jwt
from auth.schemas.login import LoginSchema
from auth.schemas.registration import RegistrationSchema
from auth.schemas.update_config import UpdateConfigSchema
from auth.services.user import UserService
from main import app, GLOBAL_ROUTE
from utils import create_subrouter

SUBROUTE = '/user'

subrouter = create_subrouter(f'{GLOBAL_ROUTE}{SUBROUTE}')
user_service = UserService()


@app.post(subrouter('/login'))
async def login(login_data: LoginSchema = Body()):
    user, token, is_password_valid = await user_service.login(**login_data.dict())
    if user is None:
        raise HTTPException(status_code=400, detail='User by this email is not found')
    if not is_password_valid:
        raise HTTPException(status_code=400, detail='Password is incorrect')
    return LoginDTO(token=token, user=UserDTO.from_orm(user))


@app.post(subrouter('/register'), status_code=201)
async def register(registration_data: RegistrationSchema = Body()):
    await user_service.register(**registration_data.dict())
    return 'Successfully registered'

@app.patch(subrouter('/config'), dependencies=[Depends(verify_jwt)])
async def update_config(request: Request, user_config: UpdateConfigSchema = Body()):
    user_id = request.state.user_id
    user = await user_service.update_config(user_id=user_id, **user_config.dict())
    return UserDTO.from_orm(user)

@app.get(subrouter(''), dependencies=[Depends(verify_jwt)])
async def get_user(request: Request):
    user_id = request.state.user_id
    user = await user_service.get_by_id(user_id)
    return UserDTO.from_orm(user)


@app.get(subrouter('/search'), dependencies=[Depends(verify_jwt)])
async def search(username: str):
    users, count = await user_service.search_users(username)
    return UsersDTO(count=count, payload=list(map(UsersPayload.from_orm, users)))