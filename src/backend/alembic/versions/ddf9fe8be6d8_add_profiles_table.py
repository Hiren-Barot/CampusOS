"""add profiles table

Revision ID: ddf9fe8be6d8
Revises: a4701a964228
Create Date: 2026-09-30 13:40:58.884816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddf9fe8be6d8'
down_revision: Union[str, None] = 'a4701a964228'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('enrollment_no', sa.String(length=50), nullable=True),
    sa.Column('course', sa.String(length=100), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.Column('admission_year', sa.Integer(), nullable=True),
    sa.Column('parent_name', sa.String(length=100), nullable=True),
    sa.Column('parent_phone', sa.String(length=20), nullable=True),
    sa.Column('qualification', sa.String(length=100), nullable=True),
    sa.Column('specialization', sa.String(length=100), nullable=True),
    sa.Column('experience_years', sa.Integer(), nullable=True),
    sa.Column('joining_date', sa.Date(), nullable=True),
    sa.Column('designation', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('profiles')
