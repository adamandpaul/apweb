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

    # Cookie session config
    registry["cookie_session_timeout"] = int(
        settings.get("cookie_session_timeout", 1200)
    )
    registry["cookie_session_reissue_time"] = int(
        settings.get(
            "cookie_session_reissue_time", int(registry["cookie_session_timeout"] / 10)
        )
    )
    registry["cookie_session_secure"] = yesish(
        settings.get("cookie_session_secure") or not registry["is_develop"]
    )

    # configure dependent packages
    config.include("pyramid_exclog")
    config.include("pyramid_tm")

    if registry["is_develop"]:
        # Development specific configuration
        config.include('pyramid_mailer.debug')
        config.include("pyramid_debugtoolbar")

    else:
        # Production specific configuration
        config.include("pyramid_mailer")

    # Configure apweb
    config.include(".session")
    config.include(".login")
    config.include(".rendering")
    config.include(".authentication")
    config.include(".database")
    config.include(".redis")
    config.include(".docs")
    config.include(".view")
    config.include(".frontend")

    # Because we provide default request methods - commit to allow the
    # consuming application to overried
    config.commit()
