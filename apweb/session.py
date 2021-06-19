# -*- coding:utf-8 -*-

import binascii
import pyramid_session_redis

def includeme(config):
    registry = config.registry
    settings = config.get_settings()
    secret = (
        settings.get("session_secret", None) or
        settings["nacl_session_secret"]  # in order to be backwards compatible
    )
    secret = secret[:32]
    session_factory = pyramid_session_redis.RedisSessionFactory(
        secret,
        timeout=registry['cookie_session_timeout'],
        cookie_name=registry["cookie_session_name"],
        cookie_domain=registry["cookie_session_domain"],
        cookie_max_age=registry['cookie_session_timeout'],
        cookie_secure=registry["cookie_session_secure"],
        cookie_httponly=True,
        client_callable=lambda request, **kwargs: request.redis,
    )
    config.set_session_factory(session_factory)
