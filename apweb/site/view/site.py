# -*- coding:utf-8 -*-

from .resource import ResourceView
from apweb.utils import map_context_reify
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift


@lift()
@view_defaults(context="apweb.site.resource.Site")
@map_context_reify(
    "application_url",
    "application_deployment",
    "application_source_commit",
)
class SiteView(ResourceView):

    @reify
    def admin_summary(self):
        return [
            *super().admin_summary,
            {"title": "Application URL", "value": self.application_url},
            {"title": "Deployment", "value": self.application_deployment},
            {"title": "Source Commit", "value": self.application_source_commit},
        ]
