import re
import uuid

from auth.services.token import TokenService
from fastapi import Request, HTTPException

token_service = TokenService()


def validate_jwt_header(token: str):
    return bool(re.search(r'^Bearer (?:[\w-]*\.){2}[\w-]*$', token))


async def verify_jwt(request: Request):
    if 'Authorization' not in request.headers:
        raise HTTPException(status_code=401, detail="No token in the Auth header")
    auth_header = request.headers['Authorization']
    if not validate_jwt_header(auth_header):
        raise HTTPException(status_code=401, detail="No token in the Auth header")

    decoded, is_error, reason = token_service.check_jwt(auth_header.split(' ')[1])
    if is_error:
        raise HTTPException(status_code=401, detail=reason)
    user_id = decoded['user_id']
    request.state.user_id = uuid.UUID(user_id)
