# -*- coding:utf-8 -*-

from .utils import yesish


def includeme(config):
    """Pyramid configuration hook for apweb package

    Brings all the configuration to gether in a single include
    """
    settings = config.get_settings()
    registry = config.registry
    registry["is_develop"] = yesish(settings["is_develop"]) or False

    config.include(".rendering")
    config.include(".frontend")
    config.include(".docs")
