# -*- coding:utf-8 -*-


class APWebSiteError(Exception):
    """An Error with the site"""


class CreateUserError(APWebSiteError):
    """Was not able to create a user"""


class CreateUserErrorInvalidUserEmail(CreateUserError):
    """The user email was invalid"""


class CreateUserErrorUserExists(CreateUserError):
    """The user already exists and not able to create it again"""
