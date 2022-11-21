import uuid

from sqlalchemy import select, insert, func, update

from core.common_queries import count_select
from core.order import Order, resolve_order
from core.singleton import Singleton
from auth.models.user import UserModel


class UserRepository(Singleton):

    def register_user(self, username: str, email: str, encrypted_password: str):
        return insert(UserModel).values(username=username, email=email, password=encrypted_password)

    def get_by_id(self, id: uuid.UUID):
        return select(UserModel).filter(UserModel.id == id)

    def get_by_username(self, username: str):
        return select(UserModel).filter(UserModel.username == username)

    def get_by_email(self, email: str):
        return select(UserModel).filter(UserModel.email == email)

    def update_user_config(self, user_id: uuid.UUID, hide_toxic: bool, hide_unchecked: bool):
        return (update(UserModel)
                .where(user_id == UserModel.id)
                .values(hide_toxic=hide_toxic,
                        hide_unchecked=hide_unchecked)
                .returning(UserModel))

    def count_filtered_by_username(self, username: str):
        return (count_select(UserModel)
                .filter(UserModel.username.like(f'{username}%')))

    def filter_by_username(self, username: str, skip: int = 0, limit: int = 10 ):
        return (select(UserModel)
                .filter(UserModel.username.like(f'{username}%')))

    def filter_by_email(self, email: str, order=Order.DESC, skip: int = 0, limit: int = 10 ):
        return (select(UserModel)
                .filter(UserModel.username.like(f'{email}%'))
                .order_by(resolve_order(UserModel.username, order))
                .skip(skip)
                .limit(limit))







