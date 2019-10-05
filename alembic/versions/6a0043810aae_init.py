"""init

Revision ID: 6a0043810aae
Revises: 
Create Date: 2019-09-19 09:06:20.203897+00:00

"""


# revision identifiers, used by Alembic.
revision = '6a0043810aae'
down_revision = None
branch_labels = ('apweb',)
depends_on = None

from apweb.site.resource.orm import NAMING_CONVENTION
from alembic import op

import sqlalchemy
import sqlalchemy_utils

meta_data = sqlalchemy.schema.MetaData(naming_convention=NAMING_CONVENTION)
Base = sqlalchemy.ext.declarative.declarative_base(metadata=meta_data)


class LogEntry(Base):
    """Stores a log entry in the table ``log_entry``

    These log entries related to application level logs that are accessable from
    the admin interface. They support the capability to log against a componenet which
    is application defined.
    """

    __tablename__ = "log_entry"
    log_entry_id = sqlalchemy.Column(
        sqlalchemy_utils.UUIDType,
        primary_key=True,
        doc="UUID: **PK** a unique identifier for the log entry",
    )
    timestamp = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=False), doc="DateTime: The time the log was emited"
    )
    component = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        index=True,
        doc="Unicode: The component the log was emited from",
    )
    level = sqlalchemy.Column(sqlalchemy.Integer, doc="The integer level of the log")
    message = sqlalchemy.Column(sqlalchemy.UnicodeText, doc="The log message")


class Redirect(Base):
    """Stores a redirect entry in the table ``redirect``

    Redirects are consulted with a not found response is handled. This table
    stores the current site redirects
    """

    __tablename__ = "redirect"
    request_path = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        primary_key=True,
        doc="The URL path the redirect matches",
    )
    request_query_string = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        primary_key=True,
        doc="The URL query string component that the request must match",
    )
    redirect_to = sqlalchemy.Column(
        sqlalchemy.Unicode(2048), doc="The URL to redirect a browser to"
    )


class User(Base):
    """Stores login user information in the table ``user``

    Information which relates to authenticating a user is stored in this table
    """

    __tablename__ = "user"

    # Identifiables.
    user_uuid = sqlalchemy.Column(
        sqlalchemy_utils.UUIDType,
        primary_key=True,
        doc="""Immuitable. A unique UUID used for users in the case where the privacy of an email needs to be protected""",
    )
    user_email = sqlalchemy.Column(
        sqlalchemy.Unicode(2048),
        unique=True,
        doc="""Unicode: The email address is used as a component to identifiy a user. It is no longer used as the id throughout the system
        and should be subtituted for a user_uuid as soon as possible. There are some corner cases where the user_email needs to be
        referenced such as granting emergency access from configruation rather then the database. But this should be rare.
        """,
    )
    password_hash = sqlalchemy.Column(
        sqlalchemy.LargeBinary,
        doc="""Bytes: The pasword hash used for authentication""",
    )
    password_reset_token = sqlalchemy.Column(
        sqlalchemy.Unicode(32),
        index=True,
        doc="""Unicode: One-time use token needed to reset a password""",
    )
    password_reset_expiry = sqlalchemy.Column(
        sqlalchemy.DateTime, doc="""DateTime: When the password_reset_token expires"""
    )
    workflow_state = sqlalchemy.Column(
        sqlalchemy.Unicode(2048), doc="Unicode: The workflow state of the user"
    )


class UserGroups(Base):
    """Stores mappings from users to groups in the table ``user_groups``
    """

    __tablename__ = "user_groups"
    user_uuid = sqlalchemy.Column(
        sqlalchemy_utils.UUIDType,
        primary_key=True,
        doc="UUID: The user uuid to map to a group",
    )
    group_id = sqlalchemy.Column(
        sqlalchemy.Unicode(2048), primary_key=True, doc="Unicode: The group id."
    )


def upgrade():
    bind = op.get_bind()
    assert 'user' not in bind.engine.table_names()
    Base.metadata.create_all(bind)


def downgrade():
    Base.drop_all()
    pass
