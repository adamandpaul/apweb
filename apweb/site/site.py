# -*- coding:utf-8 -*-

from .. import utils
from . import orm
from . import users
from contextplus import resource

import contextplus
import pyramid_mailer
import redis
import sqlalchemy
import transaction
import zope.sqlalchemy


class Site(contextplus.Site):
    """A primitive site"""

    @resource("users")
    def get_user_collection(self):
        return users.UserCollection(parent=self, name="users")

    def __init__(self, *args, mailer=None, transaction_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailer = mailer
        self.transaction_manager = transaction_manager

    @classmethod
    def from_settings(cls, settings, **kwargs):
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

        class MailerTmp(pyramid_mailer.Mailer):
            def __init__(self, **kw):
                super().__init__(transaction_manager=tm, **kw)

        mailer = MailerTmp.from_settings(settings, "mail.")

        return cls(
            settings=settings,
            db_session=db_session,
            redis=redis_instance,
            mailer=mailer,
            transaction_manager=tm,
            **kwargs,
        )

    @classmethod
    def from_request(cls, request, **kwargs):
        """Create a site object from a request object"""
        return cls(
            settings=request.registry.settings,
            db_session=request.db_session,
            redis=request.redis,
            mailer=request.mailer,
            transaction_manager=request.tm,
            **kwargs,
        )

    def set_redirect(self, path, query_string, redirect):
        """Set a redirect for a given url.

        The query string is re-ordered to be alphebetical. UTM paramitors are striped.

        Args:
            path (str): The path to match for a redirecting request
            query_string (str): The query string to match for a redirecting request
        """
        query_string = query_string or ""
        assert f"{path}?{query_string}".strip("?") != redirect.strip("?")
        query_string = utils.normalize_query_string(
            query_string, ignore_prefixes=["utm_"]
        )
        assert f"{path}?{query_string}".strip("?") != redirect.strip("?")
        redirect = orm.Redirect(
            request_path=path, request_query_string=query_string, redirect_to=redirect
        )
        self.db_session.merge(redirect)

    def get_redirect(self, path, query_string):
        """Retreive a redirect for a given path and query string

        Args:
            path (str): The path to match for a redirecting request
            query_string (str): The query string to match for a redirecting request
        """
        if not self.get_database_is_inited():
            return None
        query_string = utils.normalize_query_string(
            query_string, ignore_prefixes=["utm_"]
        )
        redirects = (
            self.db_session.query(orm.Redirect)
            .filter_by(request_path=path)
            .filter(
                sqlalchemy.sql.expression.text(
                    ":input_query_string LIKE (request_query_string || '%')"
                ).bindparams(input_query_string=query_string)
            )
        )

        redirects = sorted(
            redirects, key=lambda r: len(r.request_query_string) * -1
        )  # longest query string match first
        if len(redirects) > 0:
            return redirects[0].redirect_to
        else:
            return None

    def list_redirects(self):
        """Return a list of current redirects"""
        return self.db_session.query(orm.Redirect)
