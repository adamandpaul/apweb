# -*- coding:utf-8 -*-

from . import test
from pyramid.exceptions import HTTPForbidden
from pyramid.exceptions import HTTPNotFound
from unittest import TestCase


class TestTestView(TestCase):
    def setUp(self):
        self.view = test.TestView(None, None)

    def test_fail(self):
        with self.assertRaises(Exception):
            self.view.fail()

    def test_forbidden(self):
        with self.assertRaises(HTTPForbidden):
            self.view.forbidden()

    def test_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.view.not_found()
