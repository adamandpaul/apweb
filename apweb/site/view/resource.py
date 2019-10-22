# -*- coding:utf-8 -*-

from pyramid.decorator import reify
from pyramid.renderers import null_renderer
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_defaults(context="contextplus.Base")
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
        name="manage-info",
        renderer="jsend",
        permission="manage",
        request_method="GET",
    )
    def view_manage(self):
        return self.manage_info

    @view_config(
        route_name="api",
        name="admin-info",
        renderer="jsend",
        permission="admin-access",
        request_method="GET",
    )
    def view_admin(self):
        return {
            "description": self.description,
            "breadcrumbs": self.admin_breadcrumbs,
            "views": self.admin_views,
        }

    @view_config(
        route_name="api",
        name="resource-info",
        renderer="jsend",
        permission="admin-access",
        request_method="GET",
    )
    def view_resource_info(self):
        """Information for this resource. For use in the admin default page"""
        return {
            'summary': self.resource_info_summary,
            'views': {
                'default': self.default,
                'manage-info': self.manage_info,
            },
        }

    @view_config(
        name="internal-admin-tile",
        renderer=null_renderer,
        permission="admin-access",
    )
    def view_internal_admin_tile(self):
        return self.admin_tile

    @reify
    def default(self):
        """Public Information"""
        return {
            'name': self.name,
        }

    @reify
    def manage_info(self):
        """Information for people responsible for this resource"""
        return {
            **self.default
        }

    @reify
    def name(self):
        return self.context.name

    @reify
    def title(self):
        return self.context.title

    @reify
    def description(self):
        return self.context.description

    @reify
    def admin_views(self):
        return {
            'info': {
                'sort_key': 0,
                'title': 'Info',
                'api': '@@resource-info',
                'ui': 'view-resource-info',
            },
        }

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
    def admin_tile(self):
        return {
            "title": self.title,
            "path": self.context.path_names,
        }

    @reify
    def resource_info_summary(self):
        """Return a list of summary information"""
        summary = []
        if self.name is not None:
            summary.append({
                    "title": "URL Name",
                    "value": self.name,
            })
        if self.title is not None:
            summary.append({
                "title": "Title",
                "value": self.title,
            })
        if self.description is not None:
            summary.append({
                "title": "Description",
                "value": self.description,
            })
        return summary
