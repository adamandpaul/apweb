# -*- coding:utf-8 -*-

from .utils import yesish
from pyramid.authorization import ACLAuthorizationPolicy

import logging
import pyramid_mailer


logger = logging.getLogger("apweb.configure")


def root_factory(request):
    """Return a new root"""
    return request.site


class DefaultSiteFactory(object):
    """Default Site"""


def site_factory(request):
    """Return a default site factory"""
    return DefaultSiteFactory()


def includeme(config):
    """Pyramid configuration hook for apweb package

    Brings all the configuration to gether in a single include
    """
    logger.debug("Configuring apweb...")

    settings = config.get_settings()
    registry = config.registry

    # Extra settings
    config.add_settings({"tm.manager_hook": "pyramid_tm.explicit_manager"})

    # is_develop
    registry["is_develop"] = yesish(settings["is_develop"]) or False
    if registry["is_develop"]:
        logger.info("Running application in develop mode")

    # site factory
    config.add_request_method(site_factory, "site", reify=True)

    # root factory
    config.set_root_factory(root_factory)

    # Authorization Policy
    config.set_authorization_policy(ACLAuthorizationPolicy())

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
    config.include(".login")
    config.include(".authentication")
    config.include(".database")
    config.include(".docs")
    config.include(".view")
    config.include(".frontend")

    # Because we provide default request methods - commit to allow the
    # consuming application to overried
    config.commit()
