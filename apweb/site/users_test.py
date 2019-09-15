# -*- coding:utf-8 -*-

from . import users
from unittest import TestCase
from unittest.mock import MagicMock


class TestUser(TestCase):
    def test_init(self):
        record = MagicMock()
        u = users.User(record=record)
        self.assertEqual(u._record, record)


class TestUserCollection(TestCase):
    def test_init(self):
        collection = users.UserCollection()
        self.assertIsNotNone(collection)
