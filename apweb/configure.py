# -*- coding:utf-8 -*-

from .utils import yesish


def includeme(config):
    """Pyramid configuration hook for apweb package

    Configures the application in the following way:

    - Adds a /++frontend++ route
    """
    settings = config.get_settings()
    registry = config.registry
    registry["is_develop"] = yesish(settings["is_develop"]) or False

    # Add static route
    if registry["is_develop"]:
        config.add_static_view(
            "++frontend++", settings["frontend_static_location"], cache_max_age=5
        )
    else:
        config.add_static_view(
            "++frontend++", settings["frontend_static_location"], cache_max_age=600
        )

    config.include(".docs")
