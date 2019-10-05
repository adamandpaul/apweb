# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestIncludeme(TestCase):
    def test_includeme(self):
        config = MagicMock()
        configure.includeme(config)
        config.add_view.assert_called_with(
            None,
            name="password-login-form",
            renderer="templates/password-login-form.pt",
        )
        config.include.assert_any_call(".admin")
        config.scan.assert_called_with()
