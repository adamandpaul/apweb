# -*- coding:utf-8 -*-

from .site import Site
from unittest import TestCase


class TestSite(TestCase):
    def test_init(self):
        site = Site()
        self.assertIsNotNone(site)
