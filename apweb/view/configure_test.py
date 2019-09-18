# -*- coding:utf-8 -*-

from . import api_cors
from . import configure
from unittest import TestCase
from unittest.mock import MagicMock

import pyramid.events


class TestConfigure(TestCase):
    def test_includeme(self):
        config = MagicMock()
        config.registry = {"is_develop": False}
        configure.includeme(config)

        config.add_route.assert_any_call("check", "/_check/*traverse")
        config.add_route.assert_any_call("test", "/_test/*traverse")

        config.add_route.assert_any_call(
            "api_options", "/api/*path", request_method="OPTIONS"
        )
        config.add_subscriber.assert_any_call(
            api_cors.new_request_handler, pyramid.events.NewRequest
        )
        config.add_route.assert_any_call("api", "/api/*traverse")

        config.register_template_layer.assert_called_with("apweb.view:templates")

        config.scan.assert_called_with(ignore="apweb.view.error_develop")
