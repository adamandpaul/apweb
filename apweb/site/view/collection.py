# -*- coding:utf-8 -*-

from .resource import ResourceView
from .utils import describe_schema
from pyramid.view import view_config
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_defaults
from venusian import lift


@view_defaults(context="contextplus.Collection")
@lift()
class CollectionView(ResourceView):
    """An api view of a collection object"""

    schema_factory_add = None

    @reify
    def schema_add(self):
        if self.schema_factory_add is None:
            return None
        else:
            schema = self.schema_factory_add()
            self.bind_schema(schema)
            return schema

    @view_config(
        name="schema-add", route_name="api", renderer="jsend", permission="add", request_method="GET"
    )
    def view_schema_add(self):
        if self.schema_add is None:
            raise HTTPNotFound()
        if self.schema_add is not None:
            return describe_schema(self.schema_add)

    @view_config(
        route_name="api", renderer="jsend", permission="add", request_method="POST"
    )
    def view_add(self):
        kwargs = self.schema_add.deserialize(self.request.json)
        self.add(**kwargs)

    def add(self, **kwargs):
        self.context.add(**kwargs)

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
