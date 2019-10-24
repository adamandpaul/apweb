# -*- coding:utf-8 -*-

from pyramid.view import render_view_to_response
from pyramid.decorator import reify
from venusian import lift

import apweb.view.session


@lift()
class SessionView(apweb.view.session.SessionView):
    @reify
    def user(self):
        view = render_view_to_response(self.request.user, self.request, "internal-view", secure=False)
        return view.manage

    @reify
    def info(self):
        return {**super().info, "user": self.user}
