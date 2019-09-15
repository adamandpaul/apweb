# -*- coding:utf-8 -*-

from . import site


def site_factory(request):
    """Return a default site factory"""
    return site.Site.from_request(request)


def includeme(config):
    """A site configureation"""
    config.include("apweb")
    config.add_request_method(site_factory, "site", reify=True)
    config.commit()
