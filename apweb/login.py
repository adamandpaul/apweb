# -*- coding:utf-8 -*-

from zope.interface import Interface


class ILoginProvider(Interface):
    """An interface to provide login functionality"""

    def userid_for_login_request(self, request):
        """Return a user for a login request"""


def register_login_provider(config, provider):
    config.registry.registerUtility(provider, ILoginProvider)


def includeme(config):
    config.add_directive("register_login_provider", register_login_provider)
