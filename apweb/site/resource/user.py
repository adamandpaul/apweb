# -*- coding:utf-8 -*-

from . import exc
from . import orm
from .log_entry import ComponentLogger
from .utils import is_valid_email
from apweb.utils import normalize_email
from contextplus import id_property
from contextplus import record_property
from contextplus import resource
from contextplus import SQLAlchemyCollection
from contextplus import SQLAlchemyItem
from contextplus import WorkflowBehaviour
from datetime import datetime
from datetime import timedelta
from pyramid.authorization import Allow
from pyramid.authorization import DENY_ALL
from uuid import UUID
from uuid import uuid4

import bcrypt
import re
import secrets


class User(SQLAlchemyItem, WorkflowBehaviour):
    """A User"""

    def __acl__(self):
        return [
            (Allow, f"user_uuid:{self.user_uuid}", ["view", "manage"]),
            (Allow, "role:system-owner", ["view", "admin-access", "admin-workflow", "admin-edit", "debug"]),
            DENY_ALL,
        ]

    @property
    def title(self):
        return f"Login: {self.user_email}"

    @property
    def description(self):
        value = self.workflow_state.title() + " user"
        roles = ", ".join(self.assigned_roles)
        if roles:
            value += f' ({roles})'
        return value

    record_type = orm.User
    id_fields = ("user_uuid",)

    workflow_default_state = "active"
    workflow_transitions = {
        "ban": {"from": ("active",), "to": "banned"},
        "reinstate": {"from": ("banned",), "to": "active"},
    }

    user_uuid = id_property("user_uuid")
    user_email = record_property("user_email")
    password_reset_token = record_property("password_reset_token")
    password_reset_expiry = record_property("password_reset_expiry")

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
        (Allow, "role:system-owner", ["view", "add", "admin-access", "admin-add", "debug"]),
        DENY_ALL,
    ]

    child_type = User
    title = "User Logins"
    description = "Users logins are entities identifiable by an email."

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
        user_email = normalize_email(user_email, self.acquire.user_email_store_lower_case)
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
        if not user_email:
            return None
            
        user_uuid = (
            self.acquire.db_session.query(orm.User.user_uuid)
            .filter_by(user_email=user_email)
            .scalar()
        )
        if user_uuid is not None:
            return self[str(user_uuid)]

        # Try again with the normalized email
        user_email = normalize_email(user_email)
        user_uuid = (
            self.acquire.db_session.query(orm.User.user_uuid)
            .filter_by(user_email=user_email)
            .scalar()
        )
        if user_uuid is not None:
            return self[str(user_uuid)]

        return None

    @resource("me")
    def get_me(self):
        """Get the current user"""
        return self.acquire.get_current_user()

    @property
    def roles(self):
        query = (
            self.acquire.db_session.query(orm.RoleAssignment.role)
            .group_by(orm.RoleAssignment.role)
            .order_by(orm.RoleAssignment.role)
        )
        return list(t[0] for t in query)