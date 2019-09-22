# -*- coding:utf-8 -*-

from .utils import yesish

import binascii
import pyramid_nacl_session


def includeme(config):
    registry = config.registry
    settings = config.get_settings()
    secret_hex = settings.get("nacl_session_secret", None)
    if not secret_hex:
        secret = pyramid_nacl_session.generate_secret()
    else:
        secret = binascii.unhexlify(secret_hex)
    session_factory = pyramid_nacl_session.EncryptedCookieSessionFactory(
        secret,
        secure=registry["cookie_session_secure"],
        httponly=True,
        max_age=registry["cookie_session_timeout"],
        timeout=registry["cookie_session_timeout"],
        reissue_time=registry["cookie_session_reissue_time"],
    )
    config.set_session_factory(session_factory)
