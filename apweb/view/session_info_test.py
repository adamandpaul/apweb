# -*- coding:utf-8 -*-

from . import session_info
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestSessionInfo(TestCase):
    def setUp(self):
        self.context = context = MagicMock()
        self.request = request = MagicMock()
        request.registry = {
            "cookie_session_timeout": 111,
            "cookie_session_secure": True,
        }
        self.response = request.response
        self.view = session_info.SessionInfo(context, request)

    def test_info(self):
        self.assertEqual(self.view.info, {})

    @patch("pyramid.csrf.get_csrf_token")
    def test_set_cookie_csrf_token(self, get_csrf_token):
        self.view.set_cookie_csrf_token()
        get_csrf_token.assert_called_with(self.request)
        token = get_csrf_token.return_value
        self.response.set_cookie.assert_called_with(
            "csrf_token", token, max_age=111, secure=True, httponly=False
        )

    def test_get_authtkt(self):
        self.request.auth_policy_name_for_request = "authtkt"
        self.view.set_cookie_csrf_token = MagicMock()
        self.view.get()
        self.view.set_cookie_csrf_token.assert_called()
