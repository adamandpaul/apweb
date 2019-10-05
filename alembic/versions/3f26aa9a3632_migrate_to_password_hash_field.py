"""migrate to password_hash field

Revision ID: 3f26aa9a3632
Revises: ca549e3a86d6
Create Date: 2019-10-05 07:02:26.408897+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f26aa9a3632'
down_revision = 'ca549e3a86d6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('password_hash', sa.LargeBinary))
    op.execute("""
        UPDATE "user" set password_hash = password::bytea;
    """)

def downgrade():
    op.drop_column('user', 'password_hash')
