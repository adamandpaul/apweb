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


@view_defaults(context="contextplus.RecordItem")
@lift()
class RecordItemView(ResourceView):
    """An api view of a resource object"""

    # this will likely need to be a property in order
    # to return resonable default values
    schema_edit = None

    @view_config(route_name="api", renderer="jsend", permission="edit", request_method="PATCH")
    @view_config(route_name="api", renderer="jsend", name="admin-edit", permission="admin-edit", request_method="PATCH")
    def view_edit(self):
        """Edit a record resource"""
        if self.schema_edit is None:
            raise HTTPNotFound()
        kwargs = self.request.json
        jsonschema.validate(instance=kwargs, schema=self.schema_edit)
        child_view = self.edit(**kwargs)
        return {}

    @view_config(route_name="api", renderer="jsend", name="schema-edit", permission="edit", request_method="GET")
    def view_schema_edit(self):
        return serve_schema(self.schema_edit)

    def edit(self, **kwargs):
        self.context.edit(**kwargs)

    @reify
    def admin_views(self):
        views = {**super().admin_views}
        if self.schema_edit is not None:
            views["edit"] = {
                "sort_key": 50,
                "title": "Edit",
                "api": "@@schema-edit",
                "ui": "resource-tab-edit",
            }
        return views
