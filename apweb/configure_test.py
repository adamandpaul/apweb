# -*- coding:utf-8 -*-

from . import configure
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestIncludemeDevelop(TestCase):
    def setUp(self):
        self.settings = {
            "is_develop": "yes",
            "frontend_static_location": "/foo/bar",
            "docs_static_location": "/path/docs",
        }
        self.config = MagicMock()
        self.config.get_settings.return_value = self.settings
        self.config.registry = (
            {}
        )  # this is a simplification, the reigstry is more then a dictionary
        self.registry = self.config.registry

    @patch("apweb.configure.ACLAuthorizationPolicy")
    @patch("apweb.configure.pyramid_mailer")
    def test_includeme(self, pyramid_mailer, ACLAuthorizationPolicy):  # noqa: N803
        configure.includeme(self.config)
        c = self.config
        r = c.registry

        # Extra settings
        c.add_settings.assert_any_call(
            {"tm.manager_hook": "pyramid_tm.explicit_manager"}
        )

        # is_develop
        self.assertIs(r["is_develop"], True)

        # default site factory
        c.add_request_method(configure.site_factory, "site", reify=True)

        # root factory
        c.set_root_factory.assert_called_with(configure.root_factory)

        # authorization policy
        c.set_authorization_policy.assert_called_with(
            ACLAuthorizationPolicy.return_value
        )

        # other packages
        c.include.assert_any_call("pyramid_exclog")
        c.include.assert_any_call("pyramid_tm")
        mailer = pyramid_mailer.mailer.DummyMailer.return_value
        pyramid_mailer._set_mailer.assert_called_with(c, mailer)

        # Internal configuration
        c.include.assert_any_call(".login")
        c.include.assert_any_call(".authentication")
        c.include.assert_any_call(".database")
        c.include.assert_any_call(".redis")
        c.include.assert_any_call(".rendering")
        c.include.assert_any_call(".frontend")
        c.include.assert_any_call(".docs")
        c.include.assert_any_call(".view")

        # Make commit to config
        c.commit.assert_called_with()
