"""Pre alembic model

Revision ID: fef557a38f9a
Revises: 
Create Date: 2018-11-26 06:29:40.398773+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fef557a38f9a'
down_revision = None
branch_labels = ('apweb',)
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

from apweb.site.resource.orm import NAMING_CONVENTION
from alembic import op

import sqlalchemy
import sqlalchemy_utils


meta_data = sqlalchemy.schema.MetaData(naming_convention=NAMING_CONVENTION)
Base = sqlalchemy.ext.declarative.declarative_base(metadata=meta_data)


class LogEntry(Base):
    __tablename__ = 'log_entry'
    log_entry_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType, primary_key=True)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    component = sqlalchemy.Column(sqlalchemy.Unicode(2048), index=True)
    level = sqlalchemy.Column(sqlalchemy.Integer)
    message = sqlalchemy.Column(sqlalchemy.UnicodeText)


class Contract(Base):
    __tablename__ = 'contract'
    contract_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType, primary_key=True)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    archive_timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    other_party_session_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType)
    other_party_user_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType)
    other_party_email = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    other_party_phone = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    other_party_name = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    other_party_business_name = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    other_party_address = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    manager = sqlalchemy.Column(sqlalchemy.Unicode(2048))
    start_timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    end_timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))


class AcceptedContractVersion(Base):
    __tablename__ = 'accepted_contract_version'
    accepted_contract_version_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType, primary_key=True)
    contract_id = sqlalchemy.Column(sqlalchemy_utils.UUIDType)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    details = sqlalchemy.Column(sqlalchemy.JSON().with_variant(sqlalchemy.TEXT, 'sqlite'))


class Redirect(Base):
    __tablename__ = 'redirect'
    request_path = sqlalchemy.Column(sqlalchemy.Unicode(2048), primary_key=True)
    request_query_string = sqlalchemy.Column(sqlalchemy.Unicode(2048), primary_key=True)
    redirect_to = sqlalchemy.Column(sqlalchemy.Unicode(2048))


class User(Base):
    __tablename__ = 'user'

    # Identifiables.
    user_id = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        primary_key=True,
        doc="""Primary key for a user. Immuitable. The key requirenment for this field is that it needs to be URL safe within a url path item. Generally
        speaking this will be an email address.

        The immutability of this field means that if someone wants to change their email it requires a new user to be created. Obviously this means
        that data that needs to be retained between email address changes needs to exists on another abstracted reocrd. Such as a profile or account
        record.
        """,
    )
    user_uuid = sqlalchemy.Column(
        sqlalchemy_utils.UUIDType,
        unique=True,
        doc="""Immuitable. A unique UUID used for users in the case where the privacy of an email needs to be protected""",
    )
    api_token_hash = sqlalchemy.Column(
        sqlalchemy.LargeBinary,
        unique=True,
        doc="""The hash as secret used as an api_token""",
    )

    # Preferences
    full_name = sqlalchemy.Column(sqlalchemy.Unicode(2048), doc="""A friendly display name for the user_id""")


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade():
    Base.drop_all()
    pass
