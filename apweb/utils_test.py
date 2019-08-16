# -*- coding:utf-8 -*-

from . import utils
from unittest import TestCase


class TestYesish(TestCase):
    def test_yesish(self):
        data = [
            ("y", True),
            ("yes", True),
            ("Y", True),
            ("Yes", True),
            ("t", True),
            ("true", True),
            ("T", True),
            ("True", True),
            ("1", True),
            (1, True),
            (True, True),
            ("n", False),
            ("no", False),
            ("N", False),
            ("No", False),
            ("f", False),
            ("false", False),
            ("F", False),
            ("False", False),
            ("0", False),
            ("0", False),
            (0, False),
            (False, False),
            ("", None),
            (None, None),
        ]
        for input_value, expected_value in data:
            result = utils.yesish(input_value)
            self.assertEqual(result, expected_value)

    def test_yesish_default_value(self):
        result = utils.yesish(None, False)
        self.assertEqual(result, False)
