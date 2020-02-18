# -*- coding:utf-8 -*-
"""Behaviour for admin objects"""

from pyramid.decorator import reify
from pyramid.view import render_view_to_response
from pyramid.view import view_defaults
from pyramid.view import view_config


class AdminBehaviour(object):
    """Behaviour for objects in the administration interface"""

    @view_config(route_name="api", renderer="jsend", name="admin", permission="admin-access", request_method="GET")
    def view_admin(self):
        return {
            "title": self.title,
            "description": self.description,
            "thumbnail_url": self.admin_thumbnail_url,
            "breadcrumbs": self.admin_breadcrumbs,
            "views": self.admin_views,
            "has_workflow": self.has_workflow,
            "workflow_state": self.workflow_state,
            "workflow_actions": self.workflow_actions,
        }

    @view_config(route_name="api", renderer="jsend", name="admin-overview", permission="admin-access", request_method="GET")
    def view_admin_overview(self):
        """Information for this resource. For use in the admin default page"""
        return {
            "summary": self.admin_summary,
        }

    @view_config(route_name="api", renderer="jsend", name="workflow-action", permission="workflow", request_method="POST")
    @view_config(route_name="api", renderer="jsend", name="admin-workflow-action", permission="admin-workflow", request_method="POST")
    def view_workflow_action(self):
        if self.has_workflow:
            action = self.request.json["action"]
            if action not in self.workflow_actions:
                raise Exception("Invalid workflow action")
            workflow_from = self.context.workflow_state
            self.context.workflow_action(action)
            return {
                "from": workflow_from,
                "to": self.context.workflow_state,
            }
        raise Exception("Object does not have workflows")

    @reify
    def admin_named_resources(self):
        named_resources = []
        for named_resource in self.context.iter_named_resources():
            named_resources.append(
                {"title": named_resource.title, "path": named_resource.path_names}
            )
        return named_resources

    @reify
    def admin_links(self):
        links = []
        return links

    @reify
    def admin_breadcrumbs(self):
        """Breadcrumbs which include named resources of each ancestor"""
        breadcrumbs = []
        resources = [self.context, *self.context.iter_ancestors()]
        resources.reverse()
        for resource in resources:
            resource_view = render_view_to_response(resource, self.request, "internal-view", secure=False)
            breadcrumbs.append(
                {
                    "title": resource.title,
                    "path": resource.path_names,
                    "named_resources": resource_view.admin_named_resources,
                    "links": resource_view.admin_links,
                }
            )
        return breadcrumbs

    @reify
    def admin_views(self):
        """Dictionary and configuration tabed views on an object"""
        if self.admin_summary:
            return {
                "info": {
                    "sort_key": 0,
                    "title": "Overview",
                    "api": "@@admin-overview",
                    "default": True,
                    "ui": "resource-tab-overview",
                }
            }
        else:
            return {}

    @reify
    def admin_thumbnail_url(self):
        return None

    @reify
    def admin_summary(self):
        """Return a list of summary information"""
        return []

    @reify
    def admin_tile(self):
        return {
            "name": self.name,
            "meta_title": self.meta_title,
            "title": self.title,
            "description": self.description,
            "path": self.context.path_names,
            "thumbnail_url": self.admin_thumbnail_url,
        }