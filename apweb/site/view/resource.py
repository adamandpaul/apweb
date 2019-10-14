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
    def view_default(self):
        return self.default

    @view_config(
        route_name="api",
        name="view-manage",
        renderer="jsend",
        permission="manage",
        request_method="GET",
    )
    def view_manage(self):
        return self.manage

    @view_config(
        route_name="api",
        name="view-admin",
        renderer="jsend",
        permission="admin-access",
        request_method="GET",
    )
    def view_admin(self):
        return self.admin

    @view_config(
        route_name="api",
        name="view-debug",
        renderer="jsend",
        permission="debug",
        request_method="GET",
    )
    def view_debug(self):
        return self.debug

    @reify
    def default(self):
        """Public Information"""
        return {}

    @reify
    def manage(self):
        """Information for people responsible for this resource"""
        return {}

    @reify
    def admin(self):
        """Information for people who are responsible for the system"""
        return {"breadcrumbs": self.admin_breadcrumbs}

    @reify
    def admin_breadcrumbs(self):
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

    @reify
    def debug(self):
        """People who need to have internals for debugging"""
        return {
            'views': {
                'default': self.default,
                'manage': self.manage,
                'admin': self.admin,
            },
        }
