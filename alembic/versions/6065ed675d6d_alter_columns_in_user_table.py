"""Alter columns in user table

Revision ID: 6065ed675d6d
Revises: 51d535b8a801
Create Date: 2018-11-26 07:02:12.838780+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6065ed675d6d'
down_revision = '51d535b8a801'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('workflow_state', sa.Unicode(2048)))
    op.drop_column('user', 'full_name')


def downgrade():
    op.drop_column('user', 'workflow_state')
    op.add_column('user', sa.Column('full_name', sa.Unicode(2048)))
