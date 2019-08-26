# -*- coding:utf-8 -*-

from . import login
from unittest import TestCase
from unittest.mock import MagicMock


class TestLogin(TestCase):
    def test_register_login_provider(self):
        config = MagicMock()
        provider = MagicMock()
        login.register_login_provider(config, provider)
        config.registry.registerUtility.assert_called_with(
            provider, login.ILoginProvider
        )

    def test_includeme(self):
        config = MagicMock()
        login.includeme(config)
        config.add_directive.assert_called_with(
            "register_login_provider", login.register_login_provider
        )
