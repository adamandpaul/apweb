# -*- coding:utf-8 -*-

import redis


def get_redis(request):
    return request.registry["redis"]


def includeme(config):
    settings = config.get_settings()
    redis_instance = redis.StrictRedis.from_url(
        settings["redis_url"], decode_responses=False
    )
    config.registry["redis"] = redis_instance
    config.add_request_method(get_redis, "redis", reify=True)
