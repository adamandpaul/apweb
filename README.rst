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

``mail.*``

    Mail configuration for Pyramid Mailer

``sqlalchemy.*``

    SQLAlchemy configuration

Configuration in Application
============================

Application must configure a property on the request which returns a ``site``.
This will be added as the default root factory. e.g.::

    def site_factory(request):
        Site()

    config.add_request_method(site_factory, 'site', reify=True)

To include this package in a project. Use::

    config.include('apweb')

Provides
========

- A template layer system

- ``pyramid_tm`` with an explicit transaction manager on ``request.tm``

- ``/++docs++/`` static route for project level documentation

- ``/++frontend++/`` static route for compiled static resources.

- Additionally if ``theme.pt`` is contained in the ``frontedn_static_location``
  directory then that is injected into the template layer system

- JSON rendere extended to support ``UUID``, ``datetime``, and ``date``

- Default root factory to return ``request.site`` which is undefined in
  this package

- ``config.include("pyramid_debugtoolbar")`` if ``is_develop``. Addionally
  the side widget is monkey patched to include a button/link to ``/++docs++/``

- Setup of database engine and session factory from ``sqlalchemy.*`` config vars.
  Session exposed as ``request.db_session``

- Setup of ``pyramid_mailer`` from ``mail.*`` config vars.
