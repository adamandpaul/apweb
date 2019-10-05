# -*- coding:utf-8 -*-

from .resource import ResourceView
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift


@lift()
@view_defaults(context="apweb.site.resource.User")
class UserView(ResourceView):
    @reify
    def info_manage(self):
        u = self.context
        return {"user_email": u.user_email, "user_uuid": u.user_uuid}
