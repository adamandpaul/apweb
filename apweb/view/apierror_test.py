# -*- coding:utf-8 -*-

from . import apierror
from unittest import TestCase
from unittest.mock import MagicMock


class TestAPIErrorException(TestCase):
    def setUp(self):
        self.context = Exception()
        self.request = MagicMock()
        self.view = apierror.HandleException(self.context, self.request)

    def test_handle_exception(self):
        self.context.code = 500
        result = self.view()
        self.assertEqual(
            result,
            {"status": "error", "data": None, "code": 500, "message": "Server Error"},
        )


class TestAPIErrorClientError(TestCase):
    def setUp(self):
        self.context = Exception()
        self.context.code = 400
        self.context.jsend_data = {"foo": "123"}
        self.request = MagicMock()
        self.view = apierror.HandleClientError(self.context, self.request)

    def test_handle_exception(self):
        result = self.view()
        self.assertEqual(
            result,
            {
                "status": "fail",
                "code": 400,
                "message": "Client Error",
                "data": {"foo": "123"},
            },
        )

    def test_404(self):
        self.context.code = 404
        result = self.view()
        self.assertEqual(result["message"], "Not found")

    def test_context_message(self):
        self.context.jsend_message = "No soup"
        result = self.view()
        self.assertEqual(result["message"], "No soup")
