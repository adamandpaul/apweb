# -*- coding: utf-8 -*-

from . import rendering
from datetime import datetime
from unittest import TestCase
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import pyramid.testing


class TestRendering(TestCase):
    def setUp(self):
        self.render_globals = {"colour": "blue"}
        self.expected_render_output = "my zope blue template\n"
        super().setUp()

    @patch("apweb.rendering.get_renderer")
    def test_template_loader(self, get_renderer):
        registry = {}
        registry["templates"] = {"theme": "egg:templates/theme.pt"}
        loader = rendering.TemplateLoader(registry)
        template = loader["theme"]
        get_renderer.assert_called_with("egg:templates/theme.pt")
        self.assertEqual(
            template, get_renderer.return_value.implementation.return_value
        )

    def test_inject_templates(self):
        renderer_globals = {**self.render_globals, "request": MagicMock()}
        rendering.inject_templates(renderer_globals)
        self.assertIsInstance(renderer_globals["templates"], rendering.TemplateLoader)


class TestRenderingConfig(TestCase):
    def test_includeme(self):
        config = MagicMock()
        config.register_template_layer = None
        config.registry = {}
        rendering.includeme(config)
        self.assertEqual(config.registry["templates"], {})
        config.add_directive.assert_called_with(
            "register_template_layer", rendering.register_template_layer
        )
        config.add_subscriber.assert_has_calls(
            [
                call(rendering.inject_templates, pyramid.events.BeforeRender),
                call(rendering.inject_tools, pyramid.events.BeforeRender),
            ]
        )

    @patch("apweb.rendering.pkg_resources")
    def test_register_template_layer_dir(self, pkg_resources):
        config = MagicMock()
        config.registry = {"templates": {}}
        config.absolute_asset_spec.return_value = "egg:foo_templates"
        pkg_resources.resource_listdir.return_value = ["error.pt"]
        pkg_resources.resource_isdir.return_value = False
        rendering.register_template_layer(config, "egg:foo_templates", prefix="alt_")
        self.assertEqual(
            config.registry["templates"], {"alt_error": "egg:foo_templates/error.pt"}
        )


class TestJSONAdapters(TestCase):
    def test_json_datetime_adapter(self):
        time1 = datetime(2010, 11, 3, 7, 10)
        result = rendering.json_datetime_adapter(time1, None)
        self.assertEqual(result, "2010-11-03T07:10:00")

    def test_json_uuid_adapter(self):
        uuid1 = UUID("1804f59c-fdcd-11e8-8602-9cb6d0dde65d")
        result = rendering.json_uuid_adapter(uuid1, None)
        self.assertEqual(result, "1804f59c-fdcd-11e8-8602-9cb6d0dde65d")
