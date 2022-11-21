import json
from datetime import datetime, timezone, timedelta
from typing import Dict

import jwt
from decouple import config

from core.singleton import Singleton


class TokenService(Singleton):

    def __init__(self):
        self.secret = config('JWT_SECRET')
        self.algorithm = config('JWT_ALGORITHM', default="HS256")
        self.jwt_exp_seconds = config('JWT_EXP_SECONDS', default=86400, cast=int)

    def generate_jwt(self, payload: Dict):
        payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(seconds=self.jwt_exp_seconds)
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def check_jwt(self, token: str):
        is_error = False
        reason = None
        decoded = None
        try:
            decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            is_error = True
            reason = 'Token is Expired'
        except jwt.PyJWTError:
            is_error = True
            reason = 'Token is invalid'
        return decoded, is_error, reason

