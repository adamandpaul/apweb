# -*- coding:utf-8 -*-

from .site import Site
from unittest import TestCase
from unittest.mock import MagicMock


class TestSite(TestCase):
    def test_init(self):
        mailer = MagicMock()
        tm = MagicMock()
        site = Site(mailer=mailer, transaction_manager=tm)
        self.assertEqual(site.mailer, mailer)
        self.assertEqual(site.transaction_manager, tm)
