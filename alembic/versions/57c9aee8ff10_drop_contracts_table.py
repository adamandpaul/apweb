"""Drop contracts table

Revision ID: 57c9aee8ff10
Revises: daea19c3f7de
Create Date: 2018-11-26 07:25:01.574425+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57c9aee8ff10'
down_revision = 'daea19c3f7de'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('accepted_contract_version')
    op.drop_table('contract')


def downgrade():
    raise NotImplementedError()
