# -*- coding:utf-8 -*-

from . import api_cors
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestAPICors(TestCase):
    def test_add_headers(self):
        response = MagicMock()
        api_cors.add_headers(None, response)
        response.headers.update.assert_called_with(api_cors.DEFAULT_CORS_HEADERS)

    @patch("apweb.utils.PATTERN_API_DOMAIN")
    def test_new_request_handler_api_domain(self, pattern_api_domain):
        event = MagicMock()
        pattern_api_domain.match.return_value = "foo"
        api_cors.new_request_handler(event)
        event.request.add_response_callback(api_cors.add_headers)

    @patch("apweb.utils.PATTERN_API_DOMAIN")
    def test_new_request_handler_non_api_domain(self, pattern_api_domain):
        event = MagicMock()
        pattern_api_domain.match.return_value = None
        api_cors.new_request_handler(event)
        event.request.assert_not_called()

    def test_preflight(self):
        request = MagicMock()
        result = api_cors.preflight(None, request)
        self.assertEqual(result, request.response)
