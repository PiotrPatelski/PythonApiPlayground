"""add last few columns to posts table

Revision ID: f4cc01061c25
Revises: 979082cbdc8e
Create Date: 2023-08-29 20:04:31.624033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4cc01061c25'
down_revision: Union[str, None] = '979082cbdc8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column(
                      'published',
                      sa.Boolean(),
                      nullable=False,
                      server_default='TRUE'))
    op.add_column('posts',
                  sa.Column(
                      'created_at',
                      sa.TIMESTAMP(timezone=True),
                      nullable=False,
                      server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
