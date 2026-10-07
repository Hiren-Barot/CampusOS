"""add queries table

Revision ID: 3dd4867dc048
Revises: 9afb7f9ccaac
Create Date: 2026-10-07 09:03:56.227362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd4867dc048'
down_revision: Union[str, None] = '9afb7f9ccaac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('queries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('reply', sa.Text(), nullable=True),
        sa.Column('replied_by_id', sa.Integer(), nullable=True),
        sa.Column('replied_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['replied_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_queries_id'), 'queries', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_queries_id'), table_name='queries')
    op.drop_table('queries')