# -*- coding:utf-8 -*-

from .resource import ResourceView
from apweb.utils import map_context_reify
from pyramid.decorator import reify
from pyramid.view import view_defaults
from venusian import lift


@lift()
@view_defaults(context="apweb.site.resource.Site")
@map_context_reify(
    "motd",
    "application_url",
    "application_deployment",
    "application_source_commit",
)
class SiteView(ResourceView):


    @reify
    def admin_summary(self):
        return [
            *super().admin_summary,
            {"title": "Deployment", "value": self.application_deployment},
        ]

    @reify
    def admin_debug_info(self):
        return [
            *super().admin_debug_info,
            {"title": "Application URL", "value": self.application_url},
            {"title": "Source Commit", "value": self.application_source_commit},
        ]

    @reify
    def admin_views(self):
        views = {
            **super().admin_views,
        }
        if self.motd:
            views["motd"] = {
                "sort_key": 5,
                "title": None,
                "default": True,
                "ui": "resource-tab-simple-content",
                "options": {
                    "html": self.motd
                },
            }
        return views