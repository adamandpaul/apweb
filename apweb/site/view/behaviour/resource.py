# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.renderers import null_renderer
from pyramid.view import view_defaults
from pyramid.view import view_config

class ResourceBehaviour(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name="api", renderer="jsend", permission="view", request_method="GET")
    def view_default(self):
        return self.default

    @view_config(route_name="api", renderer="jsend", name="tile", permission="view", request_method="GET")
    def view_tile(self):
        return self.tile

    @view_config(route_name="api", renderer="jsend", name="manage", permission="manage", request_method="GET")
    def view_manage(self):
        return self.manage

    @view_config(name="internal-view", renderer=null_renderer, permission="no-permission")
    def internal_view():
        """A special view designed to return the view object on a context"""
        return self

    @reify
    def default(self):
        """Public Information"""
        return {}

    @reify
    def tile(self):
        """Information useful for constructing a tile representation of the resource"""
        return {}

    @reify
    def manage(self):
        """Information for people responsible for this resource"""
        return {**self.default}

    @reify
    def name(self):
        return self.context.name

    @reify
    def title(self):
        return self.context.title

    @reify
    def description(self):
        return self.context.description
