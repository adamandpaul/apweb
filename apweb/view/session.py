# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config

import pyramid.csrf


class SessionView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def authenticated(self):
        return bool(self.request.authenticated_userid)

    @reify
    def authenticated_userid(self):
        return self.request.authenticated_userid

    @reify
    def identifiers(self):
        return self.request.identifiers

    @reify
    def groups(self):
        return self.request.groups

    @reify
    def roles(self):
        return self.request.roles

    @reify
    def info(self):
        return {
            "authenticated": self.authenticated,
            "authenticated_userid": self.authenticated_userid,
            "identifiers": self.identifiers,
            "groups": self.groups,
            "roles": self.roles,
        }

    def set_cookie_csrf_token(self):
        response = self.request.response
        registry = self.request.registry
        token = pyramid.csrf.get_csrf_token(self.request)
        response.set_cookie(
            "csrf_token",
            token,
            max_age=registry["cookie_session_timeout"],
            secure=registry["cookie_session_secure"],
            httponly=False,
        )

    @view_config(
        route_name="api",
        name="session",
        physical_path=("",),
        renderer="jsend",
        http_cache=0,
    )
    def view(self):
        if self.request.auth_policy_name_for_request == "authtkt":
            self.set_cookie_csrf_token()
        return self.info
