# -*- coding:utf-8 -*-

from .user import UserView
from pyramid.decorator import reify
from venusian import lift

import apweb.view.session


@lift()
class SessionView(apweb.view.session.SessionView):
    @reify
    def user(self):
        user_view = UserView(self.request.user, self.request)
        return user_view.info_manage

    @reify
    def info(self):
        return {**super().info, "user": self.user}
