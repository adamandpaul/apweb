# -*- coding:utf-8 -*-

import contextplus


class User(contextplus.SQLAlchemyItem):
    """A User"""


class UserCollection(contextplus.SQLAlchemyCollection):
    """A collection of users"""

    child_type = User
    title = "Users"
    description = "Users are identifiable entities by an email address and have capabilites to login"
