# -*- coding:utf-8 -*-

from . import check
from unittest import TestCase
from unittest.mock import MagicMock


class TestCheckView(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.view = check.CheckView(None, self.request)

    def test_app(self):
        result = self.view.app()
        self.assertEqual(result.status_code, 200)

    def test_db(self):
        self.request.db_session.execute.return_value.first.return_value = (1,)
        result = self.view.db()
        self.assertEqual(result.status_code, 200)
        self.request.db_session.execute.assert_called_with("select 1;")

    def test_db_fail(self):
        self.request.db_session.execute.return_value.first.side_effect = Exception()
        result = self.view.db()
        self.assertEqual(result.status_code, 500)
        self.request.db_session.execute.assert_called_with("select 1;")

    def test_redis(self):
        self.request.redis.info.return_value = {"redis_version": "123"}
        result = self.view.redis()
        self.assertEqual(result.status_code, 200)

    def test_redis_fail(self):
        self.request.redis.info.return_value = None
        result = self.view.redis()
        self.assertEqual(result.status_code, 500)
