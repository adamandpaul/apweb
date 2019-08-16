# -*- coding:utf-8 -*-


def includeme(config):
    """Pyramid configuration hook for apweb package

    Configures the application in the following way:

    - Adds a /++frontend++ route
    """
    settings = config.get_settings()

    # Add static route
    config.add_static_view("++frontend++", settings["frontend_static_location"])
