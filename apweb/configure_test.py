# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestIncludemeDevelop(TestCase):
    def setUp(self):
        self.settings = {
            "is_develop": "yes",
            "frontend_static_location": "/foo/bar",
            "docs_static_location": "/path/docs",
        }
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
        c.add_static_view.assert_any_call("++frontend++", "/foo/bar", cache_max_age=5)
        c.add_static_view.assert_any_call("++docs++", "/path/docs", cache_max_age=5)
