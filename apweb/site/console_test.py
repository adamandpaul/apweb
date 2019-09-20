# -*- coding:utf-8 -*-

from . import console
from unittest import TestCase
from unittest.mock import MagicMock


class TestAddUser(TestCase):
    def setUp(self):
        self.cmd_context = MagicMock()
        self.args = self.cmd_context.args
        self.site = self.cmd_context.site
        self.users = self.site["users"]
        self.user = self.users.add.return_value
        self.args.user_email = "foo@bar.com"
        self.args.password = None
        self.args.initiate_password_reset = False

    def test_add_user(self):
        console.add_user(self.cmd_context)
        self.site.transaction_manager.begin.assert_called()
        self.users.add.assert_called_with(user_email="foo@bar.com")
        self.user.set_password.assert_not_called()
        self.user.initiate_password_reset.assert_not_called()
        self.site.transaction_manager.commit.assert_called()

    def test_add_user_with_password(self):
        self.args.password = "supersecret"
        console.add_user(self.cmd_context)
        self.user.set_password.assert_called_with("supersecret")

    def test_add_user_with_password_reset(self):
        self.args.initiate_password_reset = True
        console.add_user(self.cmd_context)
        self.user.initiate_password_reset.assert_called_with()
