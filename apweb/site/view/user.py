# -*- coding:utf-8 -*-

from ..resource.utils import is_valid_email
from .collection import CollectionView
from .resource import ResourceView
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift


@view_defaults(context="apweb.site.resource.User")
@lift()
class UserView(ResourceView):
    @reify
    def manage(self):
        u = self.context
        return {"user_email": u.user_email, "user_uuid": u.user_uuid}


@view_defaults(context="apweb.site.resource.UserCollection")
@lift()
class UserCollectionView(CollectionView):
    schema_add = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Add User",
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
