# -*- coding:utf-8 -*-

from .utils import yesish

import pyramid_mailer


def root_factory(request):
    """Return a new root"""
    return request.site


def includeme(config):
    """Pyramid configuration hook for apweb package

    Brings all the configuration to gether in a single include
    """
    settings = config.get_settings()
    registry = config.registry

    # Extra settings
    config.add_settings({"tm.manager_hook": "pyramid_tm.explicit_manager"})

    # apweb level configure
    registry["is_develop"] = yesish(settings["is_develop"]) or False
    config.set_root_factory(root_factory)

    # configure dependent packages
    config.include("pyramid_exclog")
    config.include("pyramid_tm")

    if registry["is_develop"]:
        # Development specific configuration
        mailer = pyramid_mailer.mailer.DummyMailer()
        pyramid_mailer._set_mailer(config, mailer)

    else:
        # Production specific configuration
        config.include("pyramid_mailer")

    # Configure apweb
    config.include(".rendering")
    config.include(".frontend")
    config.include(".docs")
