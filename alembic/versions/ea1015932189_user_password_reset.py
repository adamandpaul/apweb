"""user_password_reset

Revision ID: ea1015932189
Revises: 850b0f1e816d
Create Date: 2019-04-05 01:44:25.728433+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1015932189'
down_revision = '850b0f1e816d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('password_reset_token', sa.Unicode(32)))
    op.add_column('user', sa.Column('password_reset_expiry', sa.DateTime))
    op.create_index(
        'ix_user_password_reset_token',
        'user',
        ['password_reset_token'],
        unique=False,
    )


def downgrade():
    op.drop_index('ix_user_password_reset_token', table_name='user')
    op.drop_column('user', 'password_reset_token')
    op.drop_column('user', 'password_reset_expiry')
