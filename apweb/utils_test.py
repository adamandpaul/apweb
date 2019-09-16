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


class TestNormalizeQueryString(TestCase):
    def test_normalize_query_string(self):

        data = [
            (("", []), ""),
            (("a=z&b=z&c=z", []), "a=z&b=z&c=z"),
            (("b=z&c=z&a=z", []), "a=z&b=z&c=z"),
            (("a=z&b=z&b=z", []), "a=z&b=z&b=z"),
            (("a=z&b=z&b=y", []), "a=z&b=y&b=z"),
            (("a=z&b=z&b=y&utm_blah=123", ["utm_"]), "a=z&b=y&b=z"),
        ]
        for args, expected_result in data:
            result = utils.normalize_query_string(*args)
            self.assertEqual(
                expected_result,
                result,
                f"Expected {expected_result} from normalize_querey_string from args {args}",
            )
