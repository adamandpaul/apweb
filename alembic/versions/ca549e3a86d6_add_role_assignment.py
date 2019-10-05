"""add role assignment

Revision ID: ca549e3a86d6
Revises: ea1015932189
Create Date: 2019-09-20 05:02:28.976854+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca549e3a86d6'
down_revision = 'ea1015932189'
branch_labels = None
depends_on = None

from apweb.site.resource.orm import NAMING_CONVENTION
from alembic import op

import sqlalchemy
import sqlalchemy_utils

meta_data = sqlalchemy.schema.MetaData(naming_convention=NAMING_CONVENTION)
Base = sqlalchemy.ext.declarative.declarative_base(metadata=meta_data)


class RoleAssignment(Base):
    """Stores a role assignment from a principal"""

    __tablename__ = "role_assignment"
    principal = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        doc="Unicode: The pyramid security principal e.g. user:foo@bar.com",
        primary_key=True,
    )
    role = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        doc="Unicode: The pyramid rol assignment to the principal e.g. site-administrator",
        primary_key=True,
        index=True,
    )


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade():
    Base.drop_all()
    pass
