# -*- coding:utf-8 -*-

from .utils import yesish

import logging
import pyramid_mailer


logger = logging.getLogger("apweb.configure")


def root_factory(request):
    """Return a new root"""
    return request.site


def includeme(config):
    """Pyramid configuration hook for apweb package

    Brings all the configuration to gether in a single include
    """
    logger.debug("Configuring apweb...")

    settings = config.get_settings()
    registry = config.registry

    # Extra settings
    config.add_settings({"tm.manager_hook": "pyramid_tm.explicit_manager"})

    # apweb level configure
    registry["is_develop"] = yesish(settings["is_develop"]) or False
    if registry["is_develop"]:
        logger.info("Running application in develop mode")
    config.set_root_factory(root_factory)

    # configure dependent packages
    config.include("pyramid_exclog")
    config.include("pyramid_tm")

    if registry["is_develop"]:
        # Development specific configuration
        mailer = pyramid_mailer.mailer.DummyMailer()
        pyramid_mailer._set_mailer(config, mailer)
        config.include("pyramid_debugtoolbar")

    else:
        # Production specific configuration
        config.include("pyramid_mailer")

    # Configure apweb
    config.include(".rendering")
    config.include(".frontend")
    config.include(".docs")
