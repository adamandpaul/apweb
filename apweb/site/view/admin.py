# -*- coding:utf-8 -*-

import os.path


def includeme(config):
    """Configure admin app view html and view"""
    settings = config.get_settings()
    registry = config.registry

    # get the file path of admin.html
    admin_app_path = os.path.join(settings["frontend_static_location"], "admin.html")
    registry['admin_app_path'] = admin_app_path

    # if we are in production cache the html on the registry
    if not registry["is_develop"]:
        registry['admin_app_html'] = get_admin_html(registry)
    else:
        registry['admin_app_html'] = None

    # add view
    config.add_view(view, name="admin", request_method="GET", physical_path="/", permission="admin-access")


def view(request):
    """Serve up the admin html application"""
    response = request.response
    response.body = get_admin_html(request.registry)
    response.content_type = 'text/html'
    return response


def get_admin_html(registry):
    """Helper method to dynamicly load admin.html when we are in develop mode and the html is not cached"""
    html = registry.get('admin_app_html', None)
    if html is None:
        with open(registry['admin_app_path'], "rb") as fin:
            html = fin.read()
    return html
