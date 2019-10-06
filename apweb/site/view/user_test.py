# -*- coding:utf-8 -*-

from . import user
from unittest import TestCase
from unittest.mock import MagicMock


class TestUserView(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.context = MagicMock()
        self.view = user.UserView(self.context, self.request)

    def test_info_manage(self):
        self.assertEqual(
            self.view.info_manage,
            {
                "user_email": self.context.user_email,
                "user_uuid": self.context.user_uuid,
            },
        )
