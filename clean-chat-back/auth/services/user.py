import uuid

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.user import UserModel
from auth.repos.user_repo import UserRepository
from auth.services.token import TokenService
from auth.utils.password import check_password, encrypt_password
from core.singleton import Singleton
from database import db

class UserService(Singleton):

    def __init__(self):
        self.user_repo = UserRepository()
        self.token_service = TokenService()

    def get_by_id(self, id: uuid.UUID):
        return db.fetch_one(self.user_repo.get_by_id(id))

    def register(self, username: str, email: str, password: str):
        encrypted_password = encrypt_password(password)
        return db.execute(self.user_repo.register_user(username=username,
                                                       email=email,
                                                       encrypted_password=encrypted_password))

    def update_config(self, user_id: uuid.UUID, hide_toxic: bool, hide_unchecked: bool):
        return db.fetch_one(self.user_repo.update_user_config(user_id, hide_toxic, hide_unchecked).returning(UserModel))

    async def search_users(self, username: str):
        count = await db.fetch_one(self.user_repo.count_filtered_by_username(username))
        users = await db.fetch_all(self.user_repo.filter_by_username(username))
        return users, count[0]

    async def login(self, email: str, password: str):
        user = await db.fetch_one(self.user_repo.get_by_email(email))
        is_password_valid = False
        token = None
        if user is not None:
            is_password_valid = check_password(password, user.password)
            token = self.token_service.generate_jwt({'user_id': str(user.id)})

        return user, token, is_password_valid



