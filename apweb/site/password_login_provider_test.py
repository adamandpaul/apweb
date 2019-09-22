# -*- coding:utf-8 -*-

from .password_login_provider import PasswordLoginProvider
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


@patch("apweb.site.password_login_provider.extract_http_basic_credentials")
class TestPasswordLoginProvider(TestCase):
    def setUp(self):
        self.provider = PasswordLoginProvider()
        self.request = MagicMock()
        self.site = self.request.site
        self.users = self.site["users"]
        self.user = self.users.get_user_by_email.return_value
        self.user.check_password.return_value = True
        self.user.workflow_state = "active"

    def test_successful(self, ec):
        userid = self.provider.userid_for_login_request(self.request)

        self.assertIsNotNone(userid)
        ec.assert_called_with(self.request)
        credentials = ec.return_value
        self.users.get_user_by_email.assert_called_with(credentials.username)
        self.user.check_password.assert_called_with(credentials.password)

    def test_no_creds(self, ec):
        ec.return_value = None
        userid = self.provider.userid_for_login_request(self.request)
        self.assertIsNone(userid)

    def test_no_user(self, ec):
        self.site["users"].get_user_by_email.return_value = None
        userid = self.provider.userid_for_login_request(self.request)
        self.assertIsNone(userid)

    def test_banned_user(self, ec):
        self.user.workflow_state = "banned"
        userid = self.provider.userid_for_login_request(self.request)
        self.assertIsNone(userid)

    def test_bad_password(self, ec):
        self.user.check_password.return_value = False
        userid = self.provider.userid_for_login_request(self.request)
        self.assertIsNone(userid)
