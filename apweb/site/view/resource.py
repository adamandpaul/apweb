# -*- coding:utf-8 -*-

from .behaviour import AdminBehaviour
from .behaviour import ResourceBehaviour
from pyramid.view import view_defaults
from venusian import lift


@view_defaults(context="contextplus.Base")
@lift()
class ResourceView(AdminBehaviour, ResourceBehaviour):
    """The base view for all resource objects from contextplus.Base"""
