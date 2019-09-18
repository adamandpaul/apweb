# -*- coding:utf-8 -*-

from . import error_production
from . import error_develop
from unittest import TestCase
from unittest.mock import MagicMock
from pyramid.httpexceptions import HTTPNotFound


class TestErrorView(object):

    module = None

    def test_http_exception(self):
        request = MagicMock()
        self.module.error(Exception(), request)
        self.assertEqual(request.response.status_code, 500)

    def test_http_exception(self):
        request = MagicMock()
        result = self.module.error(HTTPNotFound(), request)
        self.assertEqual(request.response.status_code, 404)

class TestErrorProduction(TestErrorView, TestCase):
    module = error_production

class TestErrorDevelop(TestErrorView, TestCase):
    module = error_develop
