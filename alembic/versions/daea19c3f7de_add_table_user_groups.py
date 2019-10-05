"""Add table user groups

Revision ID: daea19c3f7de
Revises: 6065ed675d6d
Create Date: 2018-11-26 07:20:37.493513+00:00

"""

from alembic import op

import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'daea19c3f7de'
down_revision = '6065ed675d6d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_groups',
                    sa.Column('user_uuid', sqlalchemy_utils.UUIDType, primary_key=True),
                    sa.Column('group_id', sa.Unicode(2048), primary_key=True))


def downgrade():
    op.drop_table('user_groups')
