# -*- coding:utf-8 -*-

from datetime import timedelta

import jwt


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


def includeme(config):
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
