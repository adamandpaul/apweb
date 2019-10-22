# -*- coding:utf-8 -*-

from . import exc
from . import orm
from .utils import is_valid_email
from .log_entry import ComponentLogger
from contextplus import record_property
from contextplus import resource
from contextplus import SQLAlchemyCollection
from contextplus import SQLAlchemyItem
from contextplus import WorkflowBehaviour
from datetime import datetime
from datetime import timedelta
from pyramid.security import Allow
from pyramid.security import DENY_ALL
from uuid import UUID
from uuid import uuid4

import bcrypt
import re
import secrets


class User(SQLAlchemyItem, WorkflowBehaviour):
    """A User"""

    def __acl__(self):
        return [
            (Allow, "user:{self.user_uuid}", ["view", "manage"]),
            (Allow, "role:system-owner", ["view", "admin-access", "debug"]),
            DENY_ALL,
        ]

    @property
    def title(self):
        return f"User: {self.user_email}"

    @property
    def description(self):
        return f"{self.workflow_state} user. User UUID: {self.user_uuid}"

    record_type = orm.User
    id_fields = ("user_uuid",)

    workflow_default_state = "active"
    workflow_transitions = {
        "ban": {"from": ("active",), "to": "banned"},
        "reinstate": {"from": ("banned",), "to": "active"},
    }

    user_uuid = record_property("user_uuid")
    user_email = record_property("user_email")

    #
    # Passwords
    #

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    def set_password(self, password):
        password_hash = self.hash_password(password)
        self._record.password_hash = password_hash

    def check_password(self, password):
        if not password:
            return False
        if not self._record.password_hash:
            return False
        return bcrypt.checkpw(password.encode("utf8"), self._record.password_hash)

    def initiate_password_reset(self):
        """Generates and sets the password_reset_token and
        password_reset_expiry fields, if a password reset is not yet in
        progress or has already expired.

        :raises: User.ResetInProgressError if an active reset is in progress
        """
        record = self._record
        now = datetime.utcnow()
        token = secrets.token_urlsafe(24)
        record.password_reset_token = token
        record.password_reset_expiry = now + timedelta(days=1)

    #
    # Roles
    #

    @property
    def assigned_roles(self):
        q = self.acquire.db_session.query(orm.RoleAssignment)
        q = q.filter_by(principal=f"user:{self.user_uuid}")
        return [record.role for record in q]

    def assign_role(self, role):
        assert role
        if role in self.assigned_roles:
            raise Exception(f"User already assigned to {role}")
        record = orm.RoleAssignment(principal=f"user:{self.user_uuid}", role=role)
        self.acquire.db_session.add(record)
        self.logger.info(f"Assigned role {role}")

    def revoke_role(self, role):
        assert role
        db_session = self.acquire.db_session
        q = db_session.query(orm.RoleAssignment)
        q = q.filter_by(principal=f"user:{self.user_uuid}", role=role)
        record = q.one()
        db_session.delete(record)
        self.logger.info(f"Revoked role {role}")

    #
    # Logging
    #

    @resource("logger")
    def get_logger(self):
        """Get the logger for this member"""
        component = f"user:{self.user_uuid}"
        logger = ComponentLogger(parent=self, component=component)
        return logger


class UserCollection(SQLAlchemyCollection):
    """A collection of users"""

    __acl__ = [
        (Allow, "role:system-owner", ["view", "add", "admin-access", "debug"]),
        DENY_ALL,
    ]

    child_type = User
    title = "Users"
    description = "Users are identifiable entities by an email address and have capabilites to login"

    def name_from_child(self, child):
        """Return the travseral name for the child"""
        return str(child.id["user_uuid"])

    def id_from_name(self, name):
        """Return the child record id for a given name"""
        try:
            user_uuid = UUID(name)
        except ValueError as e:
            raise TypeError("Name is not a valid user_uuid") from e
        if name != str(user_uuid):
            raise TypeError("Incorrectly formatted user_uuid")
        return {"user_uuid": user_uuid}

    def add(self, user_email):
        if not is_valid_email(user_email):
            raise exc.CreateUserErrorInvalidUserEmail()
        db_session = self.acquire.db_session
        user_exists_query = (
            db_session.query(orm.User).filter_by(user_email=user_email).exists()
        )
        user_exists = db_session.query(user_exists_query).scalar()
        if user_exists:
            raise exc.CreateUserErrorUserExists()
        user_uuid = uuid4()
        record = orm.User(user_email=user_email, user_uuid=user_uuid)
        db_session.add(record)
        user = self.child_from_record(record)
        user.logger.info(f"Created user for email {user_email}")
        return user

    def get_user_by_email(self, user_email: str):
        """Return a user from a given email address"""
        db_session = self.acquire.db_session
        user_query = db_session.query(orm.User).filter_by(user_email=user_email)
        record = user_query.one_or_none()
        if record is not None:
            return self.child_from_record(record)
        return None
