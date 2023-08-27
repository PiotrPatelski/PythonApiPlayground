"""add foreign-key to posts table

Revision ID: 979082cbdc8e
Revises: 694ec2113991
Create Date: 2023-08-29 19:58:37.128011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '979082cbdc8e'
down_revision: Union[str, None] = '694ec2113991'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
