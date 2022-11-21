from sqlalchemy import select, func


def count_select(model):
    return select([func.count()]).select_from(model)
