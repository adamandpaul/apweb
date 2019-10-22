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

    @view_config(
        name="schema-add", route_name="api", renderer="jsend", permission="add", request_method="GET"
    )
    def view_schema_add(self):
        schema = self.schema_add
        if schema is None:
            raise HTTPNotFound()
        return self.schema_add

    @view_config(
        route_name="api", renderer="jsend", permission="add", request_method="POST"
    )
    def view_add(self):
        if self.schema_add is None:
            raise HTTPNotFound()
        else:
            kwargs = self.request.json
            jsonschema.validate(instance=kwargs, schema=self.schema_add)
            child = self.add(**kwargs)
            return render_view_to_response(child, self.request, name='internal-admin-tile')

    def add(self, **kwargs):
        return self.context.add(**kwargs)

    @reify
    def admin_views(self):
        views = {**super().admin_views}
        if self.schema_add is not None and self.request.has_permission('add'):
            views['add'] = {
                'sort_key': 60,
                'title': 'Add',
                'api': '@@schema-add',
                'ui': 'view-add-child',
            }
        return views
