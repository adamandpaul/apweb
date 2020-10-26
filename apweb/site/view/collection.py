# -*- coding:utf-8 -*-

from .utils import serve_schema
from .resource import ResourceView
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import render_view_to_response
from pyramid.view import view_config
from pyramid.view import view_defaults
from venusian import lift

import jsonschema


@view_defaults(context="contextplus.Collection")
@lift()
class CollectionView(ResourceView):
    """An api view of a collection object"""

    schema_add = None
    schema_search = None

    @view_config(route_name="api", renderer="jsend", permission="add", request_method="POST")
    @view_config(route_name="api", renderer="jsend", name="admin-add", permission="admin-add", request_method="POST")
    def view_add(self):
        """Add a child to this collection"""
        is_admin = self.request.view_name == "admin-add"
        if self.schema_add is None:
            raise HTTPNotFound()
        kwargs = self.request.json

        # Change empty string for numeric field to None
        for field, schema in self.schema_add["properties"].items():
            numeric_type = (
                type(schema["type"]) == list and
                "null" in schema["type"] and
                "integer" in schema["type"] or "numeric" in schema["type"]
            )
            if field in kwargs and numeric_type and kwargs[field] == "":
                kwargs[field] = None

        jsonschema.validate(instance=kwargs, schema=self.schema_add)
        child_view = self.add(**kwargs)
        if is_admin:
            return child_view.admin_tile
        else:
            return child_view.tile

    @view_config(route_name="api", renderer="jsend", name="schema-add", permission="add", request_method="GET")
    def view_schema_add(self):
        return serve_schema(self.schema_add)

    @view_config(name="search", route_name="api", renderer="jsend", permission="view", request_method="GET")
    @view_config(name="admin-search", route_name="api", renderer="jsend", permission="admin-access", request_method="GET")
    def view_search(self):
        schema = self.schema_search
        is_admin = self.request.view_name == "admin-search"
        if schema is not None:
            kwargs = dict(self.request.params)
            jsonschema.validate(instance=kwargs, schema=self.schema_search)
        else:
            kwargs = {
                'limit': self.request.params.get('limit', 100),
                'offset': self.request.params.get('offset', 0),
            }

        kwargs.setdefault('limit', 100)
        kwargs.setdefault('offset', 0)

        # convert views into tiles
        tiles = []
        results = self.search(**kwargs)
        for view in results['items']:
            if is_admin:
                tiles.append(view.admin_tile)
            else:
                tiles.append(view.tile)
        return {
            "total": results['total'],
            "items": tiles,
        }

    @view_config(
        name="schema-search",
        route_name="api",
        renderer="jsend",
        permission="view",
        request_method="GET",
    )
    def view_schema_search(self):
        return {
            "schema_search": serve_schema(self.schema_search),
            "schema_add": serve_schema(self.schema_add, required=False),
        }

    @view_config(
        name="admin-browse",
        route_name="api",
        renderer="jsend",
        permission="admin-access",
        request_method="GET",
    )
    def view_admin_browse(self):
        return {
            "schema_search": serve_schema(self.schema_search),
            "schema_add": serve_schema(self.schema_add, required=False),
            "title": self.title,
        }

    @reify
    def admin_views(self):
        views = {**super().admin_views}
        if self.schema_add is not None and self.request.has_permission("admin-add") and not self.schema_search:
            views["add"] = {
                "sort_key": 60,
                "title": "Add",
                "api": "@@schema-add",
                "ui": "resource-tab-add",
            }
        if self.request.has_permission("admin-access"):
            if self.schema_search is not None:
                views["find"] = {
                    "sort_key": 30,
                    "title": "Search",
                    "api": "@@schema-search",
                    "default": True,
                    "ui": "resource-tab-search",
                }
            else:
                views["find"] = {
                    "sort_key": 25,
                    "title": "Contents",
                    "api": None,
                    "default": True,
                    "ui": "resource-tab-contents",
                }
        return views

    def add(self, **kwargs):
        child = self.context.add(**kwargs)
        child_view = render_view_to_response(child, self.request, "internal-view", secure=False)
        return child_view

    def search(self, limit, offset, criteria=None, **kwargs):
        # construct critera - we only support filter_by criteria
        # other criteria can be consumed by decendent views
        criteria = criteria or []
        supported_filter_types = ['filter_by', 'sub_string']
        for key, value in kwargs.items():
            key_parts = key.split(':')
            if len(key_parts) > 1 and key_parts[0] in supported_filter_types:
                if value:
                    field = key.split(':', 1)[1]
                    criteria.append({
                        'type': key_parts[0],
                        'field': field,
                        'value': value,
                    })
            else:
                if value:
                    criteria.append({
                        'type': key,
                        'value': value,
                    })

        # Perform search
        results = self.context.filter(
            criteria=criteria,
            limit=int(limit),
            offset=int(offset),
        )

        # Convert results into view objects
        views = []
        for child in results['items']:
            view = render_view_to_response(child, self.request, "internal-view", secure=False)
            views.append(view)
        return {
            "total": results["total"],
            "items": views,
        }
