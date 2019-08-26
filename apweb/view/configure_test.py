# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock


class TestConfigure(TestCase):
    def test_includeme(self):
        config = MagicMock()
        configure.includeme(config)
        config.add_route.assert_called_with("api", "/api")
        config.scan.assert_called_with()
