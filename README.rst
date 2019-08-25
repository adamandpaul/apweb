==============
AP Web (apweb)
==============

Package to keep all the best resuable parts of our Pyramid applications.

Configuration Settings
======================

``is_develop`` (default: False)
    Indicates that the application is to be run in development mode.

``frontend_static_location`` (required)
    The compiled frontend files which will be served under ``/++frontend++``

``docs_static_location`` (default: None)
    The compiled project documentation HTML files which will be served under
    ``/++docs++``.  When in non develop mode the user requires the permission
    ``project-docs`` on the site root to be able to view.

``mail.*`` (default: defined by Pyramid Mailer)
    Mail configuration for Pyramid Mailer

``sqlalchemy.*`` (default: defined by sqlalchemy ``engine_from_config``)
    SQLAlchemy configuration

``jwt_private_key`` (default: None)
    THe JSON Web Token private key

``jwt_public_key`` (default: None)
    The JSON Web Token public key

``jwt_algorithm`` (default: None)
    The JWT algorithm used.

    ``generate_jwt`` and ``jwt_claims`` will raise an assertion error if this
    is left as None

``jwt_leeway`` (default: 10)
    token leeway

``jwt_access_ttl`` (default: 60 * 60 * 24 (one day))
    Timelimit on access tokens

``jwt_refresh_ttl`` (default: 60 * 60 * 24 * 365 (one year))
    Timelimit on refresh tokens

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

- Sets Authorization policy to ``ACLAuthorizationPolicy()``

- JSON Web Token (jwt) methods on request object:

  - ``request.jwt_claims`` returns the current validated JWT

  - ``request.generate_jwt`` creates and returns a signed JWT

- Sets up default pyramid csrf options except to exclude csrf when JSON Web
  Tokens authentication is expected.
