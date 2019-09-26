# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config


class ResourceView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def info(self):
        """Public Information"""
        return {}

    @reify
    def info_manage(self):
        """Information for people responsible for this resource"""
        return {}

    @reify
    def info_admin(self):
        """Information for people who are responsible for the system"""
        return {}

    @reify
    def info_debug(self):
        """People who need to have internals for debugging"""
        return {}

    @view_config(
        route_name="api", renderer="jsend", permission="view", request_method="get"
    )
    def view(self):
        return self.info

    @view_config(
        route_name="api",
        name="view-manage",
        renderer="jsend",
        permission="manage",
        request_method="get",
    )
    def view_manage(self):
        return {**self.view(), **self.info_manage}

    @view_config(
        route_name="api",
        name="view-admin",
        renderer="jsend",
        permission="admin",
        request_method="get",
    )
    def view_admin(self):
        return {**self.view_manage(), **self.info_admin}

    @view_config(
        route_name="api",
        name="view-debug",
        renderer="jsend",
        permission="debug",
        request_method="get",
    )
    def view_debug(self):
        return {**self.view_admin(), **self.info_debug}
