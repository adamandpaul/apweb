# -*- coding: utf-8 -*-

from . import rendering
from datetime import date
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


class TestConfigureTemplateLayers(TestCase):
    def test_configure_template_layers(self):
        config = MagicMock()
        config.register_template_layer = None
        config.registry = {}
        rendering.configure_template_layers(config)
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


class TestRenderingConfig(TestCase):
    @patch("apweb.rendering.configure_template_layers")
    @patch("apweb.rendering.configure_json_renderer")
    def test_includeme(self, c1, c2):
        config = MagicMock()
        rendering.includeme(config)
        c1.assert_called_with(config)
        c2.assert_called_with(config)


class TestJSON(TestCase):
    def test_json_datetime_adapter(self):
        time1 = datetime(2010, 11, 3, 7, 10)
        result = rendering.json_datetime_adapter(time1, None)
        self.assertEqual(result, "2010-11-03T07:10:00")

    def test_json_uuid_adapter(self):
        uuid1 = UUID("1804f59c-fdcd-11e8-8602-9cb6d0dde65d")
        result = rendering.json_uuid_adapter(uuid1, None)
        self.assertEqual(result, "1804f59c-fdcd-11e8-8602-9cb6d0dde65d")

    @patch("pyramid.renderers.render")
    def test_jsend_renderer(self, render):
        renderer = rendering.JSendRenderer({})
        result = renderer({"foo"}, {"request": "req"})
        self.assertEqual(result, render.return_value)
        render.assert_called_with("json", {"status": "success", "data": {"foo"}}, "req")

    @patch("pyramid.renderers.JSON")
    def test_configure_json_renderer(self, JSON):  # noqa: N803
        config = MagicMock()
        rendering.configure_json_renderer(config)
        json_renderer = JSON.return_value
        json_renderer.add_adapter.assert_any_call(UUID, rendering.json_uuid_adapter)
        json_renderer.add_adapter.assert_any_call(date, rendering.json_datetime_adapter)
        json_renderer.add_adapter.assert_any_call(
            datetime, rendering.json_datetime_adapter
        )
        config.add_renderer.assert_any_call("json", json_renderer)
        config.add_renderer.assert_any_call("jsend", rendering.JSendRenderer)
