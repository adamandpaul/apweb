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

    config.include(".frontend")
    config.include(".docs")
