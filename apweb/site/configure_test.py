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


class TestRequestMethods(TestCase):
    def test_get_user_for_unauthenticated_userid(self):
        request = MagicMock()
        request.unauthenticated_userid = 'foo@blah.com'
        result = configure.get_user_for_unauthenticated_userid(request)
        self.assertEqual(result, request.site["users"].get_user_by_email.return_value)
        request.site["users"].get_user_by_email.assert_called_with('foo@blah.com')

    def test_get_roles(self):
        request = MagicMock()
        request.user.assigned_roles = ['one', 'two']
        result = configure.get_roles(request)
        self.assertEqual(result, ['one', 'two'])


class TestIncludeme(TestCase):
    @patch("apweb.site.configure.PasswordLoginProvider")
    def test_includeme(self, PasswordLoginProvider):
        config = MagicMock()
        configure.includeme(config)
        config.include.assert_called_with("apweb")
        config.add_request_method.assert_any_call(
            configure.site_factory, "site", reify=True
        )
        config.add_request_method.assert_any_call(
            configure.get_user_for_unauthenticated_userid, "user", reify=True
        )
        config.add_request_method.assert_any_call(
            configure.get_roles, "roles", reify=True
        )
        config.register_login_provider.assert_called_with(
            PasswordLoginProvider.return_value
        )
        config.commit.assert_called_with()
