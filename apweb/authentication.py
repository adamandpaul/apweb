# -*- coding: utf-8 -*-
"""Sessions and authorization configuration for pyramid"""

from datetime import timedelta
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Authenticated
from pyramid.security import Everyone
from zope.interface import implementer

import binascii
import jwt
import logging
import pyramid_nacl_session


logger = logging.getLogger("apweb")


# Policy Chooser

def get_auth_policy_for_domain(request):
    """Determin which policy should be used for authentication"""
    domain = request.domain
    if domain.startswith("api.") or domain == "127.0.0.1":
        return "jwt"
    return "session"


# CSRF Protection


def should_check_csrf(request):
    """Determine if the csrf token should be checked"""
    return request.auth_policy_for_domain == "session"


# JSON Web Token


def get_jwt_claims(request):
    """Return the JSON web token claim from the request object.

    Only supports public/private key pair forms of JWT and must have
    request.registry.jwt_public_key and request.registry_jwt_algorithm defined.

    A registry.jwt_leeway (timedelta) can be defined. By default it is 10 seconds

    Args:
        request: A pyramid request object

    Returns:
        dict: The claims dictionary if a verified JWT was found
        None: Indicats that there was not valid JWT token given
    """

    # Check that we have a public key
    public_key = request.registry["jwt_public_key"]
    algorithm = request.registry["jwt_algorithm"]
    if not public_key or not algorithm:
        return None
    leeway = request.registry["jwt_leeway"]

    # Extract raw token
    auth_type, token = request.authorization or (None, None)
    if auth_type != "Bearer":
        return None
    if token is None:
        return None

    claims = jwt.decode(
        token,
        key=public_key,
        algorithms=[algorithm],
        leeway=leeway,
        options={"verify_aud": False},
    )  # we verify the aud claim in the authentication policy

    return claims


def generate_jwt(request, **claims):
    """Generate a JSON Web Token (JWT) with the given claims.

    THe token generated contains the claims signed with request.registry.private_key
    using the algorithm request.registry.algorithm

    Returns:
        str: The encoded and signed json web token
    """
    private_key = request.registry["jwt_private_key"]
    algorithm = request.registry["jwt_algorithm"]
    assert private_key is not None
    assert algorithm is not None
    token_bytes = jwt.encode(claims, key=private_key, algorithm=algorithm)
    return token_bytes.decode()


def configure_jwt(config):
    """Add request property ``jwt_claims`` and method ``generatew_jwt``"""
    settings = config.get_settings()
    registry = config.registry
    registry["jwt_private_key"] = settings.get("jwt_private_key", None)
    registry["jwt_public_key"] = settings.get("jwt_public_key", None)
    registry["jwt_algorithm"] = settings.get("jwt_algorithm", None)
    registry["jwt_leeway"] = timedelta(
        seconds=int(settings.get("jwt_leeway", None) or 10)
    )
    registry["jwt_access_ttl"] = timedelta(
        seconds=int(settings.get("jwt_access_ttl", None) or 60 * 60 * 24)
    )
    registry["jwt_refresh_ttl"] = timedelta(
        seconds=int(settings.get("jwt_refresh_ttl", None) or 60 * 60 * 24 * 365)
    )
    config.add_request_method(get_jwt_claims, "jwt_claims", reify=True)
    config.add_request_method(generate_jwt, "generate_jwt")


# Authentication Policies


@implementer(IAuthenticationPolicy)
class BrowserSessionAuthenticationPolicy(SessionAuthenticationPolicy):
    """Authentication policy for on page browser sessions"""

    def unauthenticated_userid(self, request):
        """Extract the userid from the session object"""
        return request.session.get(self.userid_key, None)


@implementer(IAuthenticationPolicy)
class JWTAuthenticationPolicy(object):
    """Authentication policy for API based requests"""

    def unauthenticated_userid(self, request):
        """Extract a userid from a jwt token"""
        claims = request.jwt_claims
        if claims is None:
            return None

        # Check for the claim of an access token
        if "access" in claims.get("aud", []):
            return claims.get("sub", None)
        else:
            return None

    def authenticated_userid(self, request):
        raise NotImplementedError()

    def effective_principals(self, request, userid=None):
        raise NotImplementedError()

    def remember(self, request, userid, **kw):
        raise NotImplementedError()

    def forget(self, request):
        raise NotImplementedError()


@implementer(IAuthenticationPolicy)
class AuthenticationPolicy(object):
    """Global authentication policy"""

    def __init__(self):
        self.jwt_policy = JWTAuthenticationPolicy()
        self.browser_session_policy = BrowserSessionAuthenticationPolicy()

    def policy(self, request):
        if request.auth_policy_for_domain == "jwt":
            return self.jwt_policy
        elif request.auth_policy_for_domain == "session":
            return self.browser_session_policy
        else:
            raise Exception("Unknown authentication policy")

    def unauthenticated_userid(self, request):
        """Proxy unauthenticated_userid method to the auth policy for this request"""
        policy = self.policy(request)
        request.auth_policy_for_domain = policy.__class__.__name__
        return self.policy(request).unauthenticated_userid(request)

    def remember(self, request, userid, **kw):
        """Proxy remember method to the auth policy for this request"""
        self.policy(request).remember(request, userid, **kw)

    def forget(self, request):
        """Proxy forget method to the auth policy for this request"""
        self.policy(request).forget(request)

    def authenticated_userid(self, request):
        userid = self.unauthenticated_userid(request)
        if Authenticated in self.effective_principals(request, userid=userid):
            return userid
        else:
            return None

    def effective_principals(self, request, userid=None):
        """Set the effective principals"""
        userid = userid or self.unauthenticated_userid(request)
        principals = [Everyone, *request.principals_for_userid]
        return principals


# include me


def includeme(config):
    """Configure pyramid to use ACL authorization and use sessions"""
    settings = config.get_settings()
    registry = config.registry

    # method to determin which auth policy to use
    config.add_request_method(get_auth_policy_for_domain, 'auth_policy_for_domain', reify=True)

    # setup csrf
    config.set_default_csrf_options(callback=should_check_csrf)

    # setup jwt
    registry["jwt_private_key"] = settings.get("jwt_private_key", None)
    registry["jwt_public_key"] = settings.get("jwt_public_key", None)
    registry["jwt_algorithm"] = settings.get("jwt_algorithm", None)
    registry["jwt_leeway"] = timedelta(
        seconds=int(settings.get("jwt_leeway", None) or 10)
    )
    registry["jwt_access_ttl"] = timedelta(
        seconds=int(settings.get("jwt_access_ttl", None) or 60 * 60 * 24)
    )
    registry["jwt_refresh_ttl"] = timedelta(
        seconds=int(settings.get("jwt_refresh_ttl", None) or 60 * 60 * 24 * 365)
    )
    config.add_request_method(get_jwt_claims, "jwt_claims", reify=True)
    config.add_request_method(generate_jwt, "generate_jwt")

    # setup sessions
    session_secret = binascii.unhexlify(
        settings["pyramid_nacl_session.session_secret"].strip()
    )
    session_max_age = int(settings.get("pyramid_nacl_session.max_age", 1200))
    session_reissue_time = int(settings.get("pyramid_nacl_session.reissue_time", 60))
    session_factory = pyramid_nacl_session.EncryptedCookieSessionFactory(
        session_secret,
        secure=not registry["is_develop"],
        httponly=True,
        max_age=session_max_age,
        timeout=session_max_age,
        reissue_time=session_reissue_time,
    )
    config.set_session_factory(session_factory)

    # Setup authenitcation
    authentication_policy = AuthenticationPolicy()
    config.set_authentication_policy(authentication_policy)
