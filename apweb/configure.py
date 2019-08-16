# -*- coding:utf-8 -*-

from .utils import yesish


def root_factory(request):
    """Return a new root"""
    return request.site


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

    # set the root factory to be the same as the site
    config.set_root_factory(root_factory)
