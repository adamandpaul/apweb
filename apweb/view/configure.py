# -*- coding:utf-8 -*-

from . import api_cors

import pyramid.events


def includeme(config):
    """Configure view"""

    # check and test routes
    config.add_route("check", "/_check/*traverse")
    config.add_route("test", "/_test/*traverse")

    # api routes and cors handeling
    config.add_route("api_options", "/api/*path", request_method="OPTIONS")
    config.add_subscriber(api_cors.new_request_handler, pyramid.events.NewRequest)
    config.add_route("api", "/api/*traverse")

    # default templates
    config.register_template_layer("apweb.view:templates")

    # error handeling
    if config.registry["is_debug"]:
        config.scan(ignore="apweb.view.error_non_debug")
    else:
        config.scan(ignore="apweb.view.error_debug")
