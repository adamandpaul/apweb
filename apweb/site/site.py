# -*- coding:utf-8 -*-


import contextplus
import redis
import pyramid_mailer
import sqlalchemy
import transaction
import zope.sqlalchemy


class Site(contextplus.Site):
    """A primitive site"""

    def __init__(self, *args, mailer=None, transaction_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailer = mailer
        self.transaction_manager = transaction_manager

    @classmethod
    def from_settings(cls, settings):
        """Create a site object from a dictionary of settings
        """

        tm = transaction.TransactionManager(explicit=True)

        db_engine = sqlalchemy.engine_from_config(settings, "sqlalchemy.")
        db_session_factory = sqlalchemy.orm.sessionmaker()
        db_session_factory.configure(bind=db_engine)
        db_session = db_session_factory()
        zope.sqlalchemy.register(db_session, transaction_manager=tm)

        redis_instance = redis.StrictRedis.from_url(
            settings["redis_url"], decode_responses=True
        )

        mailer = pyramid_mailer.Mailer.from_settings(settings, "mail.")

        return cls(settings=settings,
                   db_session=db_session,
                   redis=redis_instance,
                   mailer=mailer,
                   transaction_manager=tm)

    @classmethod
    def from_request(cls, request):
        """Create a site object from a request object"""
        cls(settings=request.registry.settings,
            db_session=request.db_session,
            redis=request.redis,
            mailer=request.mailer,
            transaction_manager=request.tm)
