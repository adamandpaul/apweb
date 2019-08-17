# -*- coding:utf-8 -*-
"""Database level pyramid configuration

Requires an explicit transaction manager on the request object ``request.tm``.
Configured in ``apweb.configure.includeme``
"""

import logging
import pyramid.events
import sqlalchemy
import zope.sqlalchemy


logger = logging.getLogger("apweb.database")


def db_session_from_request(request):
    """Create a dbsession for a given request"""
    db_session_factory = request.registry["db_session_factory"]
    db_session = db_session_factory()
    zope.sqlalchemy.register(db_session, transaction_manager=request.tm)
    return db_session


def run_orm_configure_mappers():
    """Ensure all the configure mappers are loaded"""
    sqlalchemy.orm.configure_mappers()


def includeme(config):
    """Configure the database"""

    # Create engine and session factory
    db_engine = sqlalchemy.engine_from_config(config.get_settings(), "sqlalchemy.")
    logger.debug(f"Database connection: {db_engine.url}")
    db_session_factory = sqlalchemy.orm.sessionmaker()
    db_session_factory.configure(bind=db_engine)
    config.registry["db_engine"] = db_engine
    config.registry["db_session_factory"] = db_session_factory

    # Add db_session to requests
    config.add_request_method(db_session_from_request, "db_session", reify=True)

    # Add event to ensure all the orm config mappers are loaded
    config.add_subscriber(run_orm_configure_mappers, pyramid.events.ApplicationCreated)
