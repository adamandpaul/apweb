# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.view import view_config


class ResourceView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        route_name="api", renderer="jsend", permission="view", request_method="GET"
    )
    def view(self):
        return self.info

    @view_config(
        route_name="api",
        name="view-manage",
        renderer="jsend",
        permission="manage",
        request_method="GET",
    )
    def view_manage(self):
        return {**self.view(), **self.info_manage}

    @view_config(
        route_name="api",
        name="view-admin",
        renderer="jsend",
        permission="admin-access",
        request_method="GET",
    )
    def view_admin(self):
        return {**self.view_manage(), "admin": self.info_admin}

    @view_config(
        route_name="api",
        name="view-debug",
        renderer="jsend",
        permission="debug",
        request_method="GET",
    )
    def view_debug(self):
        return {**self.view_admin(), "debug": self.info_debug}

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
        return {"breadcrumbs": self.breadcrumbs_admin}

    @reify
    def info_debug(self):
        """People who need to have internals for debugging"""
        return {}

    @reify
    def breadcrumbs_admin(self):
        """Breadcrumbs which include named resources of each ancestor"""
        breadcrumbs = []
        resources = [self.context, *self.context.iter_ancestors()]
        resources.reverse()
        for resource in resources:
            named_resources = []
            for named_resource in resource.iter_named_resources():
                named_resources.append(
                    {"title": named_resource.title, "path": named_resource.path_names}
                )

            breadcrumbs.append(
                {
                    "title": resource.title,
                    "path": resource.path_names,
                    "named_resources": named_resources,
                }
            )
        return breadcrumbs
