# -*- coding:utf-8 -*-

from ..resource.utils import is_valid_email
from .collection import CollectionView
from .resource import ResourceView
from apweb.utils import map_context_reify
from pyramid.decorator import reify
from pyramid.view import view_defaults
from pyramid.view import view_config
from venusian import lift


@view_defaults(context="apweb.site.resource.User")
@lift()
@map_context_reify(
    "assigned_roles",
)
class UserView(ResourceView):

    @reify
    def manage(self):
        u = self.context
        return {"user_email": u.user_email, "user_uuid": u.user_uuid}

    @reify
    def admin_views(self):
        views = {**super().admin_views}
        views["roles"] = {
            "sort_key": 69,
            "title": "Roles",
            "ui": "resource-tab-user-roles",
            "api": "@@admin-assigned-roles",
        }
        return views

    @view_config(route_name="api", renderer="jsend", name="admin-assigned-roles", request_method="GET", permission="admin-access")
    def view_admin_assigned_roles(self):
        assigned_roles = self.assigned_roles
        current_roles = list(self.context.parent.roles)
        current_roles.sort(key=lambda t: (t not in assigned_roles, t))
        return {
            "assigned_roles": assigned_roles,
            "current_roles": current_roles,
        }

    @view_config(route_name="api", renderer="jsend", name="admin-assign-role", request_method="POST", permission="admin-edit")
    def view_admin_roles_add(self):
        role = self.request.json["role"]
        self.context.assign_role(role)
        return {}

    @view_config(route_name="api", renderer="jsend", name="admin-revoke-role", request_method="POST", permission="admin-edit")
    def view_admin_revoke_role(self):
        role = self.request.json["role"]
        self.context.revoke_role(role)
        return {}


@view_defaults(context="apweb.site.resource.UserCollection")
@lift()
class UserCollectionView(CollectionView):
    schema_add = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Add a user to the system",
        "type": "object",
        "properties": {
            "user_email": {
                "title": "User Email",
                "description": "An email address used to authenticate a user",
                "type": "string",
            }
        },
        "required": ["user_email"],
    }

    schema_search = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "sub_string:user_email": {
                "title": "User Email",
                "description": "An email address used to authenticate a user",
                "type": "string",
                "x-add-field": "user_email",
            },
            "filter_by:workflow_state": {
                "title": "Workflow State",
                "type": "string",
                "enum": ["active", "banned"],
            },
        },
    }
