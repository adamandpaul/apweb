# -*- coding:utf-8 -*-

from . import orm
from contextplus import record_property
from contextplus import SQLAlchemyCollection
from contextplus import SQLAlchemyItem
from contextplus import WorkflowBehaviour

import bcrypt
import re


# VALID_USER_EMAIL checks for a semi-validish email. Of most concern
# it will fail to validate emails with unsafe url charactors
VALID_USER_EMAIL_EXPRESSION = (
    "^"
    "[^][{}|#?/:<>%`\\\\\x00-\x1f\x7f ]"  # The first letter: url unsafe chars + space
    "[^][{}|#?/:<>%`\\\\\x00-\x1f\x7f]*"  # Letters up to @ symbol: url unstafe chars
    "@"  # an @ symbol
    "[^]\"'@[{}|#?/:<>%`\\\\\x00-\x1f\x7f ]+"  # Domain parts: url unsafe chars + space + quotes + @
    "\\."  # a dot
    "[^]\"'@[{}|#?/:<>%`\\\\\x00-\x1f\x7f ]{2,}"  # The top level: url unsafe chars + sapece + quotes + @
    "$"
)
VALID_USER_EMAIL = re.compile(VALID_USER_EMAIL_EXPRESSION)


class User(SQLAlchemyItem, WorkflowBehaviour):
    """A User"""

    @property
    def title(self):
        return f"User: {self.email}"

    @property
    def description(self):
        return f"{self.workflow_state} user. User UUID: {self.user_uuid}"

    record_type = orm.User
    id_fields = ("user_uuid",)

    workflow_default_tate = "active"
    workflow_transitions = {
        "ban": {"from": ("active",), "to": "banned"},
        "reinstate": {"from": ("banned",), "to": "active"},
    }

    user_uuid = record_property("user_uuid")
    user_email = record_property("user_email")

    @classmethod
    def is_user_email_valid(cls, user_email):
        """Test if a potential user_email is a valid (safe) email

        Because we use email's in our url scheme the VALID_USER_EMAIL regular expression filters
        out potential unsafe charactors.

        Args:
            user_email (str): The value to be tested

        Returns:
            bool: True if the user_email was valid. Otherwise False
        """
        if len(user_email) > 254:
            return False
        return VALID_USER_EMAIL.match(user_email) is not None

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


class UserCollection(SQLAlchemyCollection):
    """A collection of users"""

    child_type = User
    title = "Users"
    description = "Users are identifiable entities by an email address and have capabilites to login"
