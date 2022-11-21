import enum

from sqlalchemy import Column


class Order(enum.Enum):
    DESC = 'desc'
    ASC = 'asc'


def resolve_order(target: Column, order: Order):
    if order == Order.ASC:
        return target.asc()
    return target.desc()
