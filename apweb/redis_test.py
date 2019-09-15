# -*- coding:utf-8 -*-

from . import redis
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestGetRedis(TestCase):
    def test_get_redis(self):
        request = MagicMock()
        request.registry = {"redis": "a redis"}
        result = redis.get_redis(request)
        self.assertEqual(result, "a redis")


class TestIncludeme(TestCase):
    @patch("redis.StrictRedis")
    def test_includeme(self, StrictRedis):
        redis_instance = StrictRedis.from_url.return_value
        config = MagicMock()
        config.registry = {}
        config.get_settings.return_value = {"redis_url": "path/to/redis"}
        redis.includeme(config)
        StrictRedis.from_url.assert_called_with("path/to/redis", decode_responses=True)
        self.assertEqual(config.registry["redis"], redis_instance)
        config.add_request_method.assert_called_with(
            redis.get_redis, "redis", reify=True
        )
