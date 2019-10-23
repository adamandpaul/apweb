# -*- coding:utf-8 -*-

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
    def view_add(self):
        """Add a child to this collection"""
        if self.schema_add is None:
            raise HTTPNotFound()
        kwargs = self.request.json
        jsonschema.validate(instance=kwargs, schema=self.schema_add)
        child_view = self.add(**kwargs)
        return child_view.tile

    @view_config(route_name="api", renderer="jsend", name="admin-add", permission="admin-add", request_method="POST")
    def view_admin_add(self):
        """Special add that returns an admin tile"""
        if self.schema_add is None:
            raise HTTPNotFound()
        kwargs = self.request.json
        jsonschema.validate(instance=kwargs, schema=self.schema_add)
        child_view = self.add(**kwargs)
        return child_view.admin_tile

    @view_config(route_name="api", renderer="jsend", name="schema-add", permission="add", request_method="GET")
    def view_schema_add(self):
        schema = self.schema_add
        if schema is None:
            raise HTTPNotFound()
        return self.schema_add

    def add(self, **kwargs):
        child = self.context.add(**kwargs)
        child_view = render_view_to_response(child, self.request, "internal-view")
        return child_view

    @view_config(
        name="schema-search",
        route_name="api",
        renderer="jsend",
        permission="view",
        request_method="GET",
    )
    def view_schema_search(self):
        schema = self.schema_search
        if schema is None:
            raise HTTPNotFound()
        return self.schema_search

    @reify
    def admin_views(self):
        views = {**super().admin_views}
        if self.schema_add is not None and self.request.has_permission("admin-add"):
            views["add"] = {
                "sort_key": 60,
                "title": "Add",
                "api": "@@schema-add",
                "ui": "resource-tab-add",
            }
        if self.schema_search is not None and self.request.has_permission("admin-access"):
            views["find"] = {
                "sort_key": 30,
                "title": "Find",
                "api": "@@schema-search",
                "ui": "resource-tab-search",
            }

        return views
