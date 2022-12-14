"""Init db

Revision ID: a35acc246c5b
Revises: 
Create Date: 2022-11-15 22:12:44.351217

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a35acc246c5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table('channels',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('archived', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channels_name'), 'channels', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('password', sa.String(length=76), nullable=False),
    sa.Column('hide_toxic', sa.Boolean(), server_default=sa.text('TRUE'), nullable=True),
    sa.Column('hide_unchecked', sa.Boolean(), server_default=sa.text('TRUE'), nullable=True),
    sa.Column('deleted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_password'), 'users', ['password'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('messages',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('edited', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('type', sa.Enum('UNCHECKED', 'TOXIC', 'SAFE', name='messagetypeenum'), server_default='UNCHECKED', nullable=True),
    sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_content'), 'messages', ['content'], unique=False)
    op.create_table('users_to_channels',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_to_channels')
    op.drop_index(op.f('ix_messages_content'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_password'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_channels_name'), table_name='channels')
    op.drop_table('channels')
    # ### end Alembic commands ###
