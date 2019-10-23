# -*- coding:utf-8 -*-
"""Behaviour for admin objects"""

from pyramid.decorator import reify
from pyramid.view import view_defaults
from pyramid.view import view_config


class AdminBehaviour(object):
    """Behaviour for objects in the administration interface"""

    @view_config(route_name="api", renderer="jsend", name="admin", permission="admin-access", request_method="GET")
    def view_admin(self):
        return {
            "description": self.description,
            "breadcrumbs": self.admin_breadcrumbs,
            "views": self.admin_views,
        }

    @view_config(route_name="api", renderer="jsend", name="admin-overview", permission="admin-access", request_method="GET")
    def view_admin_overview(self):
        """Information for this resource. For use in the admin default page"""
        return {
            "summary": self.admin_summary,
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
    def admin_views(self):
        """Dictionary and configuration tabed views on an object"""
        return {
            "info": {
                "sort_key": 0,
                "title": "Overview",
                "api": "@@admin-overview",
                "ui": "resource-tab-overview",
            }
        }

    @reify
    def admin_summary(self):
        """Return a list of summary information"""
        summary = []
        if self.name is not None:
            summary.append({"title": "URL Name", "value": self.name})
        if self.title is not None:
            summary.append({"title": "Title", "value": self.title})
        if self.description is not None:
            summary.append({"title": "Description", "value": self.description})
        return summary

    @reify
    def admin_tile(self):
        return {"title": self.title, "path": self.context.path_names}
