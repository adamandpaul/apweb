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
        self.view.__dict__["breadcrumbs_admin"] = ["app", "foo"]
        self.assertEqual(self.view.info, {})
        self.assertEqual(self.view.info_manage, {})
        self.assertEqual(self.view.info_admin, {"breadcrumbs": ["app", "foo"]})
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
            self.view.view_admin(),
            {"a": "Info", "b": "Info Manage", "admin": {"c": "Info Admin"}},
        )
        self.assertEqual(
            self.view.view_debug(),
            {
                "a": "Info",
                "b": "Info Manage",
                "admin": {"c": "Info Admin"},
                "debug": {"d": "Info Debug"},
            },
        )


class TestResourceBreadcrumbsView(TestCase):
    def setUp(self):

        root_named_resource = MagicMock()
        root_named_resource.title = "N"
        root_named_resource.path_names = ["", "n"]

        root = MagicMock()
        root.title = "A"
        root.path_names = [""]
        root.iter_named_resources.return_value = [root_named_resource]
        parent = MagicMock()
        parent.title = "P"
        parent.path_names = ["", "p"]
        context = MagicMock()
        context.title = "C"
        context.path_names = ["", "p", "c"]
        context.iter_ancestors.return_value = [parent, root]

        self.request = MagicMock()
        self.context = context
        self.view = resource.ResourceView(self.context, self.request)

    def test_breadcrumbs_admin(self):
        result = self.view.breadcrumbs_admin
        expected = [
            {
                "title": "A",
                "path": [""],
                "named_resources": [{"title": "N", "path": ["", "n"]}],
            },
            {"title": "P", "path": ["", "p"], "named_resources": []},
            {"title": "C", "path": ["", "p", "c"], "named_resources": []},
        ]
        self.assertEqual(result, expected)
