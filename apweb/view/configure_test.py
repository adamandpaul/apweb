# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestConfigure(TestCase):
    def test_includeme(self):
        config = MagicMock()
        config.registry = {"is_develop": False}
        configure.includeme(config)
        config.register_template_layer.assert_called_with("apweb.view:templates")
        config.add_route.assert_any_call("api", "/api/*traverse")
        config.add_route.assert_any_call("check", "/_check/*traverse")
        config.add_route.assert_any_call("test", "/_test/*traverse")
        config.scan.assert_called_with(ignore="apweb.view.error_develop")
