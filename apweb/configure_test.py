# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestIncludeme(TestCase):
    def setUp(self):
        self.settings = {"frontend_static_location": "/foo/bar"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings

    def test_includeme(self):
        configure.includeme(self.config)
        c = self.config
        c.add_static_view.assert_called_with("++frontend++", "/foo/bar")
