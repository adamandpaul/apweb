# -*- coding:utf-8 -*-

from ..resource.utils import is_valid_email
from .resource import ResourceView
from .collection import CollectionView
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift

import colander


def user_email_validator(ndoe, value):
    if not is_valid_email(value):
        raise colander.Invalid(node, 'Not a valid email address')


class SchemaAddUser(colander.MappingSchema):
    user_email = colander.SchemaNode(
        colander.String(),
        validator=user_email_validator,
    )


@view_defaults(context="apweb.site.resource.User")
@lift()
class UserView(ResourceView):
    @reify
    def info_manage(self):
        u = self.context
        return {"user_email": u.user_email, "user_uuid": u.user_uuid}


@view_defaults(context="apweb.site.resource.UserCollection")
@lift()
class UserCollectionView(CollectionView):
    schema_factory_add = SchemaAddUser
