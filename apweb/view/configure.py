# -*- coding:utf-8 -*-


def includeme(config):
    """Configure view"""
    config.add_route("api", "/api")
    config.scan()
