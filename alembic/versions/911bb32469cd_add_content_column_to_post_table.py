"""add content column to Post table

Revision ID: 911bb32469cd
Revises: 7882415496fd
Create Date: 2023-08-28 22:27:43.722999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '911bb32469cd'
down_revision: Union[str, None] = '7882415496fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
