"""create company table

Revision ID: 5aea75be8563
Revises: 
Create Date: 2025-03-11 16:38:41.899561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5aea75be8563'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'company',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nit', sa.String(255), nullable=False),
        sa.Column('name_company', sa.String(255), nullable=False),
        sa.Column('sector', sa.String(255), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('company')
