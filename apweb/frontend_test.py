# -*- coding:utf-8 -*-

from . import frontend
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestIncludemeDevelop(TestCase):
    def setUp(self):
        self.settings = {"frontend_static_location": "/foo/bar"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = {"is_develop": True, "templates": {}}
        self.registry = self.config.registry

    @patch("apweb.frontend.exists")
    def test_includeme(self, exists):
        exists.return_value = True
        frontend.includeme(self.config)
        c = self.config

        self.assertEqual(self.registry["templates"], {"theme": "/foo/bar/theme.pt"})
        c.add_static_view.assert_any_call("++frontend++", "/foo/bar", cache_max_age=5)


class TestIncludemeProd(TestCase):
    def setUp(self):
        self.settings = {"frontend_static_location": "/foo/bar"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = {"is_develop": False, "templates": {}}
        self.registry = self.config.registry

    def test_includeme(self):
        frontend.includeme(self.config)
        c = self.config

        c.add_static_view.assert_any_call("++frontend++", "/foo/bar", cache_max_age=600)
