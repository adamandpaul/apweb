# -*- coding:utf-8 -*-

from .password_login_provider import PasswordLoginProvider
from .resource import Site


def site_factory(request):
    """Return a default site factory"""
    return Site.from_request(request)


def get_user_for_unauthenticated_userid(request):
    email = request.unauthenticated_userid
    return request.site["users"].get_user_by_email(email)


def get_roles(request):
    user = request.user
    if user:
        return user.assigned_roles
    return []


def includeme(config):
    """A site configureation"""
    config.include("apweb")
    config.add_request_method(site_factory, "site", reify=True)
    config.add_request_method(get_user_for_unauthenticated_userid, "user", reify=True)
    config.add_request_method(get_roles, "roles", reify=True)
    config.register_login_provider(PasswordLoginProvider())
    config.include(".view")
    config.commit()
