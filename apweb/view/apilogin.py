# -*- coding:utf-8 -*-

from ..authentication.jwt import JWTNotConfiguredError
from datetime import datetime
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

import logging
import pyramid.security


logger = logging.getLogger("apweb.view.api_login")


class NotAbleToCreateLogin(Exception):
    """Was not able to create a login"""


@view_config(route_name="api", name="login", request_method="POST")
class APILogin(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def userid(self):
        return self.request.authenticated_userid

    @reify
    def jwt_iat(self):
        """datetime: The JWT iat (issued at) claism"""
        return datetime.utcnow()

    @reify
    def jwt_access_exp(self):
        """datetime: The JWT exp (expiry) claism for the access token"""
        return self.jwt_iat + self.request.registry["jwt_access_ttl"]

    @reify
    def jwt_access_token(self):
        """str: A newly JWT access toekn"""
        return self.request.generate_jwt(
            sub=self.userid, aud=["access"], iat=self.jwt_iat, exp=self.jwt_access_exp
        )

    @reify
    def jwt_refresh_exp(self):
        """datetime: The JWT exp (expiry) claism for the refresh token"""
        return self.jwt_iat + self.request.registry["jwt_refresh_ttl"]

    @reify
    def jwt_refresh_token(self):
        """str: A newly JWT refresh toekn"""
        return self.request.generate_jwt(
            sub=self.userid, aud=["refresh"], iat=self.jwt_iat, exp=self.jwt_refresh_exp
        )

    def post(self):

        # Check request paramitors
        if self.request.method.lower() != "post":
            raise HTTPForbidden("Request method not allowed")

        if not self.userid:
            raise HTTPForbidden("Was not able to login")

        # Try to create a browser session
        try:
            pyramid.security.remember(self.request, self.userid)
        except NotImplementedError:
            browser_session = False
        else:
            browser_session = True

        # Create a JWT token
        try:
            jwt_access_token = self.jwt_access_token
            jwt_refresh_token = self.jwt_refresh_token
        except JWTNotConfiguredError as e:
            jwt_access_token = None
            jwt_refresh_token = None
            if not browser_session:
                logger.warn(f"Do you need to configure JSON Web Token? {e}")

        if (
            jwt_access_token is None or jwt_refresh_token is None
        ) and not browser_session:
            raise NotAbleToCreateLogin("Unable to create jwt or login session")

        return {
            "browser_session": browser_session,
            "jwt": jwt_access_token,
            "jwt_refresh": jwt_refresh_token,
        }
