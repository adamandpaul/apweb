# -*- coding:utf-8 -*-

from . import exc
from . import orm
from .logs import ComponentLogger
from .users import User
from .users import UserCollection
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID


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
        self.db_session = MagicMock()
        self.user.db_session = self.db_session

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

    def test_initiate_password_reset(self):
        user = self.user

        # Works the first time
        user.initiate_password_reset()
        self.assertEqual(len(user._record.password_reset_token), 32)
        self.assertIsInstance(user._record.password_reset_expiry, datetime)

        # Works on subsequent times too
        user.initiate_password_reset()
        self.assertEqual(len(user._record.password_reset_token), 32)
        self.assertIsInstance(user._record.password_reset_expiry, datetime)

    def test_get_logger(self):
        logger = self.user.get_logger()
        self.assertIsInstance(logger, ComponentLogger)
        self.assertEqual(logger.component, f"user:{self.user.user_uuid}")

    def test_assigned_roles(self):
        query = self.db_session.query
        query.return_value.filterby.return_value = [
            orm.RoleAssignment(role="one"),
            orm.RoleAssignment(role="two"),
        ]
        roles = self.user.assigned_roles
        self.assertEqual(roles, ["one", "two"])
        query.assert_called_with(orm.RoleAssignment)
        q = query.return_value
        q.filterby.assert_called_with(principal=f"user:{self.user.user_uuid}")

    @patch("apweb.site.orm.RoleAssignment")
    def test_assign_role(self, RoleAssignment):
        self.user.assign_role("foo")
        RoleAssignment.assert_called_with(
            principal=f"user:{self.user.user_uuid}", role="foo"
        )
        record = RoleAssignment.return_value
        self.db_session.add.assert_any_call(record)

    def test_revoke_role(self):
        query = self.db_session.query
        record = query.return_value.filterby.return_value.one.return_value

        self.user.revoke_role("foo")

        query.assert_called_with(orm.RoleAssignment)
        q = query.return_value
        q.filterby.assert_called_with(
            principal=f"user:{self.user.user_uuid}", role="foo"
        )
        self.db_session.delete.assert_called_with(record)


class TestUserCollectionClass(TestCase):
    def test_init(self):
        collection = UserCollection()
        self.assertIsNotNone(collection)


class TestUserCollection(TestCase):
    def setUp(self):
        self.collection = UserCollection()

    def test_name_from_child(self):
        child = MagicMock()
        child.id = {"user_uuid": UUID("18dcd264-bc84-48d5-a1be-6502447619f4")}
        name = self.collection.name_from_child(child)
        self.assertEqual(name, "18dcd264-bc84-48d5-a1be-6502447619f4")

    def test_id_from_name(self):
        result = self.collection.id_from_name("18dcd264-bc84-48d5-a1be-6502447619f4")
        self.assertEqual(
            result, {"user_uuid": UUID("18dcd264-bc84-48d5-a1be-6502447619f4")}
        )

    def test_add_user(self):
        self.collection.db_session = MagicMock()
        self.collection.db_session.query.return_value.scalar.return_value = False
        user = self.collection.add("foo@noemail.adamandpaul.biz")
        self.assertEqual(user.user_email, "foo@noemail.adamandpaul.biz")

    def test_add_user_bad_email(self):
        self.collection.db_session = MagicMock()
        self.collection.db_session.query.return_value.scalar.return_value = False
        with self.assertRaises(exc.CreateUserErrorInvalidUserEmail):
            self.collection.add("bademail")

    def test_add_user_user_exists(self):
        self.collection.db_session = MagicMock()
        self.collection.db_session.query.return_value.scalar.return_value = True
        with self.assertRaises(exc.CreateUserErrorUserExists):
            self.collection.add("foo@noemail.adamandpaul.biz")
