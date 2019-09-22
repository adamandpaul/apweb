# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestSiteFactory(TestCase):
    @patch("apweb.site.site.Site")
    def test_site_factory(self, Site):
        request = MagicMock()
        configure.site_factory(request)
        Site.from_request.assert_called_with(request)


class TestIncludeme(TestCase):
    @patch("apweb.site.configure.PasswordLoginProvider")
    def test_includeme(self, PasswordLoginProvider):
        config = MagicMock()
        configure.includeme(config)
        config.include.assert_called_with("apweb")
        config.add_request_method.assert_called_with(
            configure.site_factory, "site", reify=True
        )
        config.register_login_provider.assert_called_with(
            PasswordLoginProvider.return_value
        )
        config.commit.assert_called_with()
