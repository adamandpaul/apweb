"""Rename user_id to user_email

Revision ID: 51d535b8a801
Revises: fef557a38f9a
Create Date: 2018-11-26 06:53:46.099282+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51d535b8a801'
down_revision = 'fef557a38f9a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'user_id', new_column_name='user_email')


def downgrade():
    op.alter_column('user', 'user_email', new_column_name='user_id')
