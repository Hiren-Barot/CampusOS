"""add assignment file fields

Revision ID: 9afb7f9ccaac
Revises: ddf9fe8be6d8
Create Date: 2026-10-03 12:15:06.527016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9afb7f9ccaac'
down_revision: Union[str, None] = 'ddf9fe8be6d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('assignments', sa.Column('file_path', sa.String(length=500), nullable=True))
    op.add_column('assignments', sa.Column('file_name', sa.String(length=255), nullable=True))
    op.add_column('assignments', sa.Column('file_size', sa.Integer(), nullable=True))
    op.add_column('assignments', sa.Column('file_type', sa.String(length=100), nullable=True))


def downgrade() -> None:
    op.drop_column('assignments', 'file_type')
    op.drop_column('assignments', 'file_size')
    op.drop_column('assignments', 'file_name')
    op.drop_column('assignments', 'file_path')