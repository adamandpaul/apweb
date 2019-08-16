# -*- coding:utf-8 -*-

from . import docs
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestIncludemeDevelop(TestCase):
    def setUp(self):
        self.settings = {"docs_static_location": "/path/docs"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = {"is_develop": True}
        self.registry = self.config.registry

    @patch("apweb.docs.monkey_patch_pyramid_debugtoolbar_toolbar_toolbar_html_template")
    def test_includeme(self, monkey_patch):
        docs.includeme(self.config)
        c = self.config

        monkey_patch.assert_called_with()
        c.add_static_view.assert_any_call("++docs++", "/path/docs", cache_max_age=5)


class TestIncludemeProd(TestCase):
    def setUp(self):
        self.settings = {"docs_static_location": "/path/docs"}
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = {"is_develop": False}
        self.registry = self.config.registry

    @patch("apweb.docs.monkey_patch_pyramid_debugtoolbar_toolbar_toolbar_html_template")
    def test_includeme(self, monkey_patch):
        docs.includeme(self.config)
        c = self.config

        monkey_patch.assert_called_with()
        c.add_static_view.assert_any_call(
            "++docs++", "/path/docs", permission="project-docs", cache_max_age=300
        )
