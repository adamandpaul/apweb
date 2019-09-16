# -*- coding:utf-8 -*-

from .users import User
from .users import UserCollection
from unittest import TestCase
from unittest.mock import MagicMock


class TestUserInit(TestCase):
    def test_init(self):
        record = MagicMock()
        u = User(record=record)
        self.assertEqual(u.user_uuid, record.user_uuid)
        self.assertEqual(u.user_email, record.user_email)

    def test_bad_chars_valid_user_id(self):
        bad_chars = "][{}|#?/:<>%`\x00\x10\x7f"
        for c in bad_chars:
            emails = [
                f"{c}aa@example.com",
                f"a{c}a@example.com",
                f"aa@ex{c}ample.com",
                f"aa@example.co{c}m",
            ]
            for email in emails:
                self.assertFalse(User.is_user_email_valid(email))

    def test_bad_valid_user_id(self):
        emails = [
            "",
            " ",
            "@",
            " @example.com",
            "@example.com",
            "user@ex ample.com",
            "user@examplle.c om",
            "user1@",
            'javascript:alert("helo")@example.com',
            "aa@" + ("b" * 249) + ".co",  # an email of 255 chars should be invalid
            f'aa@"example.com"',
        ]
        for email in emails:
            self.assertFalse(User.is_user_email_valid(email))

    def test_valid_user_id(self):
        emails = [
            "email@example.com",
            '"my funny quoted email"@example.com',
            '"email@user"@example.com',
            "email+tag@example.com",
            '"我吃了一个苹果"@example.com',
            "user@我吃了一个苹果.com",
            "aa@" + ("b" * 248) + ".co",  # an email of 254 chars should be valid
        ]
        for email in emails:
            self.assertTrue(User.is_user_email_valid(email))


class TestUserCollection(TestCase):
    def test_init(self):
        collection = UserCollection()
        self.assertIsNotNone(collection)
