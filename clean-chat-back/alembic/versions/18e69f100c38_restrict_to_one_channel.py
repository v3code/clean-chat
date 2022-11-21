"""Restrict to one channel

Revision ID: 18e69f100c38
Revises: a35acc246c5b
Create Date: 2022-11-16 04:19:38.107900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18e69f100c38'
down_revision = 'a35acc246c5b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO channels (name) VALUES ('main_test')")
    pass


def downgrade() -> None:
    pass
