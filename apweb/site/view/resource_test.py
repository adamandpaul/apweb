# -*- coding:utf-8 -*-

from . import resource
from unittest import TestCase
from unittest.mock import MagicMock


class TestResourceView(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.context = MagicMock()
        self.view = resource.ResourceView(self.context, self.request)

    def test_infos(self):
        self.assertEqual(self.view.info, {})
        self.assertEqual(self.view.info_manage, {})
        self.assertEqual(self.view.info_admin, {})
        self.assertEqual(self.view.info_debug, {})

    def test_gets(self):
        self.view.__dict__.update(
            {
                "info": {"a": "Info"},
                "info_manage": {"b": "Info Manage"},
                "info_admin": {"c": "Info Admin"},
                "info_debug": {"d": "Info Debug"},
            }
        )
        self.assertEqual(self.view.view(), {"a": "Info"})
        self.assertEqual(self.view.view_manage(), {"a": "Info", "b": "Info Manage"})
        self.assertEqual(
            self.view.view_admin(), {"a": "Info", "b": "Info Manage", "c": "Info Admin"}
        )
        self.assertEqual(
            self.view.view_debug(),
            {"a": "Info", "b": "Info Manage", "c": "Info Admin", "d": "Info Debug"},
        )
