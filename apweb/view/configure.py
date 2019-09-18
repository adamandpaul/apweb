# -*- coding:utf-8 -*-


def includeme(config):
    """Configure view"""
    config.add_route("api", "/api/*traverse")
    config.add_route("check", "/_check/*traverse")
    config.add_route("test", "/_test/*traverse")
    config.register_template_layer("apweb.view:templates")
    if config.registry["is_develop"]:
        config.scan(ignore="apweb.view.error_production")
    else:
        config.scan(ignore="apweb.view.error_develop")
