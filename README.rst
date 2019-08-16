==============
AP Web (apweb)
==============

Package to keep all the best resuable parts of our Pyramid applications.

Expected Configuration Settings
===============================

``is_develop``

    Indicates that the application is to be run in development mode.

``frontend_static_location``

    The compiled frontend files which will be served under ``/++frontend++``

``docs_static_location``

    The compiled project documentation HTML files which will be served under
    ``/++docs++``.  When in non develop mode the user requires the permission
    ``project-docs`` on the site root to be able to view.

Configuration in Application
============================

Application must configure a property on the request which returns a ``site``.
This will be added as the default root factory. e.g.::

    def site_factory(request):
        Site()

    config.add_request_method(site_factory, 'site', reify=True)

