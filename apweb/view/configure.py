# -*- coding:utf-8 -*-


def includeme(config):
    """Configure view"""
    config.add_route("api", "/api")
    config.register_template_layer('apweb.view:templates')
    config.scan()
