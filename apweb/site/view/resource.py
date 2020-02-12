# -*- coding:utf-8 -*-

from .behaviour import AdminBehaviour
from .behaviour import WorkflowBehaviour
from apweb.contextplus_base_view_behaviour import ContextPlusBaseViewBehaviour
from pyramid.view import view_defaults
from venusian import lift


@view_defaults(context="contextplus.Base")
@lift()
class ResourceView(AdminBehaviour, ContextPlusBaseViewBehaviour, WorkflowBehaviour):
    """The base view for all resource objects from contextplus.Base"""
