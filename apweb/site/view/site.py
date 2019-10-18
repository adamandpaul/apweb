# -*- coding:utf-8 -*-

from .resource import ResourceView
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift


@lift()
@view_defaults(context="apweb.site.resource.Site")
class SiteView(ResourceView):
    pass
