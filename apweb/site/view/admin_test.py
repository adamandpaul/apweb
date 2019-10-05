# -*- coding:utf-8 -*-

from . import admin
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestIncludeme(TestCase):

    def setUp(self):
        self.settings = settings = {
            'frontend_static_location': 'path/to/frontend',
        }
        self.registry = registry = {
            'is_develop': False
        }
        self.config = config = MagicMock()
        config.get_settings.return_value = settings
        config.registry = registry

    @patch('apweb.site.view.admin.get_admin_html')
    def test_includeme(self, get_admin_html):
        get_admin_html.return_value = 'html foo'
        c = self.config
        admin.includeme(c)
        self.assertEqual(c.registry['admin_app_path'], 'path/to/frontend/admin.html')
        get_admin_html.assert_called_with(c.registry)
        self.assertEqual(c.registry['admin_app_html'], 'html foo')
        c.add_view.assert_called_with(admin.view, name="admin", request_method="GET", physical_path="/", permission="admin-access")

    def test_includeme_develop(self):
        self.registry['is_develop'] = True
        c = self.config
        admin.includeme(c)
        self.assertIsNone(c.registry['admin_app_html'])


class TestAdmin(TestCase):

    @patch('apweb.site.view.admin.get_admin_html')
    def test_view(self, get_admin_html):
        request = MagicMock()
        response = request.response
        result = admin.view(request)
        self.assertEqual(result, response)
        get_admin_html.assert_called_with(request.registry)
        self.assertEqual(response.body, get_admin_html.return_value)
        self.assertEqual(response.content_type, 'text/html')

    @patch('apweb.site.view.admin.open')
    def test_get_admin_html(self, global_open):
        fin = global_open.return_value.__enter__.return_value
        fin.read.return_value = 'html foo'
        request = MagicMock()
        request.registry = {
            'admin_app_path': 'path/to/admin.html',
            'admin_app_html': None,
        }
        html = admin.get_admin_html(request.registry)
        global_open.assert_called_with('path/to/admin.html', 'rb')
        self.assertEqual(html, 'html foo')

    def test_get_admin_html_cached(self):
        request = MagicMock()
        request.registry = {
            'admin_app_path': 'path/to/admin.html',
            'admin_app_html': 'html bar',
        }
        html = admin.get_admin_html(request.registry)
        self.assertEqual(html, 'html bar')
