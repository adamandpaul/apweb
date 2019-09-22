# -*- coding:utf-8 -*-

from . import session
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestSession(TestCase):
    def setUp(self):
        self.config = config = MagicMock()
        self.settings = config.get_settings.return_value = {
            "nacl_session_secret": "big secret"
        }
        self.registry = config.registry = {
            "cookie_session_secure": True,
            "cookie_session_timeout": 100,
            "cookie_session_reissue_time": 10,
        }

    @patch("pyramid_nacl_session.EncryptedCookieSessionFactory")
    @patch("binascii.unhexlify")
    def test_includeme(self, unhexlify, EncryptedCookieSessionFactory):
        session.includeme(self.config)
        unhexlify.assert_called_with("big secret")
        secret = unhexlify.return_value
        EncryptedCookieSessionFactory.assert_called_with(
            secret,
            secure=True,
            httponly=True,
            max_age=100,
            timeout=100,
            reissue_time=10,
        )
        factory = EncryptedCookieSessionFactory.return_value
        self.config.set_session_factory.assert_called_with(factory)

    @patch("pyramid_nacl_session.EncryptedCookieSessionFactory")
    @patch("pyramid_nacl_session.generate_secret")
    def test_includeme_generated_secret(
        self, generate_secret, EncryptedCookieSessionFactory
    ):
        del self.settings["nacl_session_secret"]
        session.includeme(self.config)
        secret = generate_secret.return_value
        EncryptedCookieSessionFactory.assert_called_with(
            secret,
            secure=True,
            httponly=True,
            max_age=100,
            timeout=100,
            reissue_time=10,
        )
        factory = EncryptedCookieSessionFactory.return_value
        self.config.set_session_factory.assert_called_with(factory)
