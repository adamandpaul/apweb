# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestIncludeme(TestCase):
    def setUp(self):
        self.settings = {"is_develop": "yes", "frontend_static_location": "/foo/bar"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = (
            {}
        )  # this is a simplification, the reigstry is more then a dictionary
        self.registry = self.config.registry

    def test_includeme(self):
        configure.includeme(self.config)
        c = self.config
        r = c.registry

        self.assertIs(r["is_develop"], True)
        c.add_static_view.assert_called_with("++frontend++", "/foo/bar")
