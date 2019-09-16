# -*- coding:utf-8 -*-

from .users import User
from .users import UserCollection
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestUserClass(TestCase):
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

    def test_hash_password(self):
        result = User.hash_password("foo")
        self.assertNotIn("foo", result.decode("utf-8"))

    @patch("bcrypt.gensalt")
    @patch("bcrypt.hashpw")
    def test_hash_password_bcrypt(self, hashpw, gensalt):
        result = User.hash_password("foo")
        hashpw.assert_called_with(b"foo", gensalt.return_value)
        self.assertEqual(result, hashpw.return_value)


class TestUser(TestCase):
    def setUp(self):
        self.record = MagicMock()
        self.user = User(record=self.record)

    def test_set_password(self):
        self.user.hash_password = MagicMock()
        self.user.set_password("blah")
        self.assertEqual(
            self.record.password_hash, self.user.hash_password.return_value
        )

    @patch("bcrypt.checkpw")
    def test_check_password(self, checkpw):
        checkpw.return_value = True
        result = self.user.check_password("blah123")
        checkpw.assert_called_with(b"blah123", self.record.password_hash)
        self.assertTrue(result)

    @patch("bcrypt.checkpw")
    def test_check_password_fail(self, checkpw):
        checkpw.return_value = False
        result = self.user.check_password("blah123")
        checkpw.assert_called_with(b"blah123", self.record.password_hash)
        self.assertFalse(result)

    def test_check_password_empty(self):
        result = self.user.check_password("")
        self.assertFalse(result)

    def test_check_password_unset(self):
        self.record.password_hash = b""
        result = self.user.check_password("fooblah")
        self.assertFalse(result)


class TestUserCollection(TestCase):
    def test_init(self):
        collection = UserCollection()
        self.assertIsNotNone(collection)
