# -*- coding:utf-8 -*-

from . import resource
from unittest import TestCase
from unittest.mock import MagicMock


class TestResourceView(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.context = MagicMock()
        self.view = resource.ResourceView(self.context, self.request)

    def test_default_and_manage(self):
        self.assertEqual(self.view.default, {})
        self.assertEqual(self.view.manage, {})

    def test_admin(self):
        self.view.__dict__["admin_breadcrumbs"] = ["app", "foo"]
        self.assertEqual(self.view.admin, {"breadcrumbs": ["app", "foo"]})

    def test_debug(self):
        self.view.__dict__.update({"default": "ddd", "manage": "mmm", "admin": "aaa"})
        self.assertEqual(
            self.view.debug,
            {"views": {"default": "ddd", "manage": "mmm", "admin": "aaa"}},
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
        result = self.view.admin_breadcrumbs
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
