"""create user table

Revision ID: 79fae018d0f2
Revises: 5aea75be8563
Create Date: 2025-03-14 13:22:52.584026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79fae018d0f2'
down_revision: Union[str, None] = '5aea75be8563'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('token', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade() -> None:
    op.drop_table('user')
