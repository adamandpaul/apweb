# -*- coding:utf-8 -*-

from apweb.utils import context_property
from pyramid.decorator import reify
from pyramid.renderers import null_renderer
from pyramid.view import view_defaults
from pyramid.view import view_config


class ContextPlusBaseViewBehaviour(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    name = context_property("name", reify=True)
    title = context_property("title", reify=True)
    description = context_property("description", reify=True)

    @reify
    def meta_title(self):
        """The meta title of the object"""
        return self.context.get_meta_title()

    @reify
    def default(self):
        """Public Information"""
        return {}

    @reify
    def tile(self):
        """Information useful for constructing a tile representation of the resource"""
        return {}

    @view_config(name="internal-view", renderer=null_renderer, permission="no-permission")
    def internal_view(self):
        """A special view designed to return the view object on a context"""
        return self

    @view_config(route_name="api", renderer="jsend", permission="view", request_method="GET")
    def view_default(self):
        return self.default

    @view_config(route_name="api", renderer="jsend", name="tile", permission="view", request_method="GET")
    def view_tile(self):
        return self.tile