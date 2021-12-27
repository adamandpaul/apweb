# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from decimal import Decimal
from pprint import pprint
from pyramid.renderers import get_renderer
from pyramid.view import render_view_to_response
from uuid import UUID

import os
import pkg_resources
import pyramid.events
import pyramid.renderers
import pyramid.security
import json


# Template layers


class TemplateLoader(object):
    """Dynamicly load templates from the template registry"""

    def __init__(self, registry):
        self._registry = registry
        self._cache = {}

    def __getitem__(self, key):
        if key in self._cache:
            return self._cache[key]
        template_path = self._registry["templates"][key]
        template = get_renderer(template_path).implementation()
        self._cache[key] = template
        return template


def register_template_layer(config, resource_spec_dir, prefix=""):
    """Add a templates to the templates registry potentially overridin any previous tempaltes"""
    resource_spec_dir = config.absolute_asset_spec(resource_spec_dir)
    package, path = resource_spec_dir.split(":")
    for item in pkg_resources.resource_listdir(package, path):
        item_path = os.path.join(path, item)
        if not pkg_resources.resource_isdir(package, item_path):
            template_key = item.split(".")[0]
            template_spec = os.path.join(resource_spec_dir, item)
            config.registry["templates"][prefix + template_key] = template_spec


def inject_template_vars(renderer_globals):
    if renderer_globals.get("request", None) is not None:
        renderer_globals["templates"] = TemplateLoader(
            renderer_globals["request"].registry
        )
    renderer_globals["render_view_to_response"] = render_view_to_response
    renderer_globals["pprint"] = pprint


def inject_tools(render_globals):
    render_globals["json"] = json


def configure_template_layers(config):
    if getattr(config, "register_template_layer", None) is None:
        config.registry["templates"] = {}
        config.add_directive("register_template_layer", register_template_layer)
        config.add_subscriber(inject_template_vars, pyramid.events.BeforeRender)
        config.add_subscriber(inject_tools, pyramid.events.BeforeRender)


# JSON Renderer


def json_datetime_adapter(obj, request):
    """Adapt datetime to JSON"""
    return obj.isoformat()


def json_uuid_adapter(obj, request):
    return str(obj)


def json_decimal_adapter(obj, request):
    return str(obj)


class JSendRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        value = {"status": "success", "data": value}
        request = system.get("request", None)
        result = pyramid.renderers.render("json", value, request)
        if request:
            response = request.response
            response.content_type = "application/json"
            response.charset = "utf-8"
        return result


def configure_json_renderer(config):

    # Add the JSON adapter for datetime
    json_renderer = pyramid.renderers.JSON()
    json_renderer.add_adapter(datetime, json_datetime_adapter)
    json_renderer.add_adapter(date, json_datetime_adapter)
    json_renderer.add_adapter(UUID, json_uuid_adapter)
    json_renderer.add_adapter(Decimal, json_decimal_adapter)
    config.add_renderer("json", json_renderer)
    config.add_renderer("jsend", JSendRenderer)


def includeme(config):
    config.include("pyramid_chameleon")
    configure_template_layers(config)
    configure_json_renderer(config)
