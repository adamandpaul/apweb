# -*- coding:utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock


class TestIncludeMe(TestCase):
    def setUp(self):
        self.config = MagicMock()
