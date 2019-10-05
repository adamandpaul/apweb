"""password field for user

Revision ID: 850b0f1e816d
Revises: 57c9aee8ff10
Create Date: 2018-12-19 07:50:29.871485+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '850b0f1e816d'
down_revision = '57c9aee8ff10'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('password', sa.Unicode(2048)))



def downgrade():
    op.drop_column('user', 'password')

