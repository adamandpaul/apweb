# -*- coding:utf-8 -*-

from os.path import exists

import os.path


def includeme(config):
    settings = config.get_settings()
    registry = config.registry

    # Add static route for frount end
    if registry["is_develop"]:
        config.add_static_view(
            "++frontend++", settings["frontend_static_location"], cache_max_age=5
        )
    else:
        config.add_static_view(
            "++frontend++", settings["frontend_static_location"], cache_max_age=600
        )

    # If there is a theme.pt file in the frontend static lcoation then use that as the
    # master theme template
    theme_path = os.path.join(settings["frontend_static_location"], "theme.pt")
    if exists(theme_path):
        registry["templates"]["theme"] = theme_path
