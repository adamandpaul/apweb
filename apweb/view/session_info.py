# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config

import pyramid.csrf


class SessionInfo(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def info(self):
        return {}

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
        route_name="api", name="session_info", physical_path=("",), renderer="jsend"
    )
    def get(self):
        if self.request.auth_policy_name_for_request == "authtkt":
            self.set_cookie_csrf_token()
        return self.info
