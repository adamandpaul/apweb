# -*- coding:utf-8 -*-

from . import api_login
from datetime import datetime
from datetime import timedelta
from pyramid.httpexceptions import HTTPForbidden
from unittest.mock import MagicMock
from unittest.mock import patch

import unittest


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.registry = {
            "jwt_access_ttl": timedelta(seconds=60),
            "jwt_refresh_ttl": timedelta(seconds=120),
        }
        self.request = MagicMock()
        self.request.registry = self.registry
        self.request.method = "post"
        self.request.authenticated_userid = None
        self.view = api_login.APILogin(None, self.request)

    def test_userid_no_login(self):
        registry = MagicMock()
        self.request.registry = registry
        registry.getAllUntilitiesRegisteredFor.return_value = []
        self.assertEqual(self.view.userid, None)

    def test_userid(self):
        registry = MagicMock()
        registry.getAllUtilitiesRegisteredFor.return_value = []
        self.request.registry = registry
        self.request.authenticated_userid = "foo@foo"
        self.assertEqual(self.view.userid, "foo@foo")

    def test_userid_from_login_provider(self):
        registry = MagicMock()
        no_user = MagicMock()
        no_user.userid_for_login_request.return_value = None
        a_user = MagicMock()
        a_user.userid_for_login_request.return_value = "bar@bar"
        registry.getAllUtilitiesRegisteredFor.return_value = [no_user, a_user]
        self.request.registry = registry
        self.request.authenticated_userid = "foo@foo"
        result = self.view.userid
        a_user.userid_for_login_request.assert_called_with(self.request)
        self.assertEqual(result, "bar@bar")

    @patch("apweb.view.api_login.datetime")
    def test_jwt_iat(self, datetime):
        self.assertEqual(self.view.jwt_iat, datetime.utcnow.return_value)

    @patch("apweb.view.api_login.datetime")
    def test_jwt_access_exp(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2000, 1, 1, 1, 0)
        self.assertEqual(self.view.jwt_access_exp, datetime(2000, 1, 1, 1, 1))

    @patch("apweb.view.api_login.datetime")
    def test_jwt_access_token(self, mock_datetime):
        self.view.__dict__["userid"] = "foo@foo"
        mock_datetime.utcnow.return_value = datetime(2000, 1, 1, 1, 0)
        generate_jwt = self.request.generate_jwt
        generate_jwt.return_value = "abc.def.hij"
        token = self.view.jwt_access_token
        self.assertEqual(token, "abc.def.hij")
        generate_jwt.assert_called_with(
            sub="foo@foo",
            aud=["access"],
            iat=datetime(2000, 1, 1, 1, 0),
            exp=datetime(2000, 1, 1, 1, 1),
        )

    @patch("apweb.view.api_login.datetime")
    def test_jwt_refresh_exp(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2000, 1, 1, 1, 0)
        self.assertEqual(self.view.jwt_refresh_exp, datetime(2000, 1, 1, 1, 2))

    @patch("apweb.view.api_login.datetime")
    def test_jwt_refresh_token(self, mock_datetime):
        self.view.__dict__["userid"] = "foo@foo"
        mock_datetime.utcnow.return_value = datetime(2000, 1, 1, 1, 0)
        generate_jwt = self.request.generate_jwt
        generate_jwt.return_value = "abc.def.hij"
        token = self.view.jwt_refresh_token
        self.assertEqual(token, "abc.def.hij")
        generate_jwt.assert_called_with(
            sub="foo@foo",
            aud=["refresh"],
            iat=datetime(2000, 1, 1, 1, 0),
            exp=datetime(2000, 1, 1, 1, 2),
        )

    def test_post_should_forbid_bad_method(self):
        self.request.method = "get"
        with self.assertRaises(HTTPForbidden):
            self.view.post()

    def test_post_should_forbid_no_userid(self):
        self.view.__dict__["userid"] = None
        with self.assertRaises(HTTPForbidden):
            self.view.post()

    @patch("pyramid.security.remember")
    def test_post(self, remember):
        self.view.__dict__["userid"] = "foo@bar"
        self.view.__dict__["jwt_access_token"] = "token 123"
        self.view.__dict__["jwt_refresh_token"] = "token abc"
        remember.return_value = ['header']
        response = self.view.post()
        remember.assert_called_with(self.request, "foo@bar")
        self.assertEqual(
            response,
            {"browser_session": True, "jwt": "token 123", "jwt_refresh": "token abc"},
        )
        self.request.response.headers.update.assert_called_with(['header'])

    @patch("pyramid.security.remember")
    def test_post_session_only(self, remember):
        self.view.__dict__["userid"] = "foo@bar"
        self.view.__dict__["jwt_access_token"] = None
        self.view.__dict__["jwt_refresh_token"] = None
        remember.return_value = ['header']
        response = self.view.post()
        remember.assert_called_with(self.request, "foo@bar")
        self.assertEqual(
            response, {"browser_session": True, "jwt": None, "jwt_refresh": None}
        )

    @patch("pyramid.security.remember")
    def test_post_jwt_only(self, remember):
        self.view.__dict__["userid"] = "foo@bar"
        self.view.__dict__["jwt_access_token"] = "token 123"
        self.view.__dict__["jwt_refresh_token"] = "token abc"
        remember.side_effect = NotImplementedError()
        response = self.view.post()
        self.assertEqual(
            response,
            {"browser_session": False, "jwt": "token 123", "jwt_refresh": "token abc"},
        )

    @patch("pyramid.security.remember")
    def test_post_unable_to_login(self, remember):
        self.view.__dict__["userid"] = "foo@bar"
        self.view.__dict__["jwt_access_token"] = None
        self.view.__dict__["jwt_refresh_token"] = None
        remember.side_effect = NotImplementedError()
        with self.assertRaises(api_login.NotAbleToCreateLogin):
            self.view.post()
