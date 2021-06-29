# -*- coding:utf-8 -*-

from os.path import exists

import logging
import os.path


logger = logging.getLogger("apweb.frontend")


def includeme(config):
    settings = config.get_settings()
    registry = config.registry

    # Add static route for frount end
    logger.info(
        f'Serving {settings["frontend_static_location"]} as static frontend location from /++static++/'
    )
    if registry["is_debug"]:
        config.add_static_view(
            "++theme++", settings["frontend_static_location"], cache_max_age=5
        )
    else:
        config.add_static_view(
            "++theme++", settings["frontend_static_location"], cache_max_age=600
        )

    # If there is a theme.pt file in the frontend static lcoation then use that as the
    # master theme template
    theme_path = os.path.join(settings["frontend_static_location"], "theme.pt")
    if exists(theme_path):
        logger.info(
            f'Found theme.pt in frontend static location folder. Using as registry["templates"]["theme"]'
        )
        registry["templates"]["theme"] = theme_path
