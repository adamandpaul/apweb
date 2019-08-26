==============
AP Web (apweb)
==============

Package to keep all the best resuable parts of our Pyramid applications.

Settings Configuration
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

``authtkt_secret`` (default: Random)
    The secret used for authtkt. If not set a randomly generated
    secret is used. This will be unworkable for production systems.

``authtkt_timeout`` (default: 1200 (20 minutes)
    The authtkt timeout.

``authtkt_reissue_time`` (default: ``authtkt_timeout`` / 10)
    The reissue time for a new ticket to be issued.

Request Configuration
=====================

Following are a set of configurations which are expected to appear on the
request. Some default configurations are provided - at the end of
``config.include('apweb')`` the ``config.commit()`` is called in order that an
application can override the default below by using
``config.add_request_method``


``request.site`` (default: ``apweb.configure.DefaultSite``)
    An object which is the site. This is used as the default root factory.
    This allows a "site" concept to exists, particularly when diferent
    plugins that traverson using different root factories mean that accessing
    an application meaningful root becomes tricky to access.

``request.user`` (default: None)
    A database sourced user object, sourced using the ``request.unauthenticated_userid``
    value.

    If ``request.user`` is not None, then the Authentication Policy defined in apweb will:

    - Return extend effective principals with: [Authenticated, ``f'user:{userid}'``]

    - Return the ``userid`` for ``request.authenticated_userid``

    If ``request.user`` is None, then the Authentication Policy defined in apweb will:

    - Not extend effective principals with: [Authenticated, ``f'user:{userid}'``]

    - Return the None for ``request.authenticated_userid``

``request.groups`` (default: ``[]``)
    A list of groups that are added to the effective principals in the format
    ``group:{group_name}``

``request.roles`` (default: ``[]``)
    A list of roles that are added to the effective principals in the format
    ``role:{role_name}``


Other Configuration
===================

``config.register_template_layer(resource_spec_dir, prefix)``
    This causes a search of the directory defined by ``resource_spec_dir``
    for templates which are added to the ``registry['templates']`` dictionary.
    E.g.::

        registry['templates'][f'{prefix}{file}'] = 'path/to/template/file.pt`

    This allows subsiquent calls of ``register_template_layer`` to override
    previously defined templates.


Provides
========

- A template layer system

- A renderer ``jsend`` for `JSend <https://github.com/omniti-labs/jsend>`_

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

- A JSON Web Token Authentication Policy

- A multi authentication policy which selects ``AuthTktAuthenticationPolicy``
  or a JWT Authentication policy based on the result of
  ``request.auth_policy_name_for_request`` The default
  ``auth_policy_name_for_request`` select JWT auth policy for requests for
  domains which start with ``api.`` or are IP addresses. Otherwise the AuthTkt
  policy is selected.

- A namespaced effective principals. E.g.:

  - ``user:userid``

  - ``group:group-name``

  - ``role:role-name``

  The authentication policy doesn't include the non namespaced effective
  principal of the userid. Incase someone regisers a username as ``role:admin``
