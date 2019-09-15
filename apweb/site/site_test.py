# -*- coding:utf-8 -*-

from .site import Site
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestSite(TestCase):
    def test_init(self):
        mailer = MagicMock()
        tm = MagicMock()
        site = Site(mailer=mailer, transaction_manager=tm)
        self.assertEqual(site.mailer, mailer)
        self.assertEqual(site.transaction_manager, tm)

    @patch('pyramid_mailer.Mailer')
    @patch('redis.StrictRedis')
    @patch('zope.sqlalchemy.register')
    @patch('sqlalchemy.orm.sessionmaker')
    @patch('sqlalchemy.engine_from_config')
    @patch('transaction.TransactionManager')
    def test_from_settings(self, TransactionManager, sa_engine_from_config, sa_sessionmaker, 
                                zope_sa_register, StrictRedis, Mailer):
        tm = TransactionManager.return_value
        db_engine = sa_engine_from_config.return_value
        db_session_factory = sa_sessionmaker.return_value
        db_session = db_session_factory.return_value
        redis = StrictRedis.from_url.return_value
        mailer = Mailer.from_settings.return_value
        settings = {'foo': 1, 'bar': 2, 'redis_url': 'path/to/redis'}
        site = Site.from_settings(settings)

        TransactionManager.assert_called_with(explicit=True)
        sa_engine_from_config.assert_called_with(settings, "sqlalchemy.")
        db_session_factory.configure.assert_called_with(bind=db_engine)
        zope_sa_register.assert_called_with(db_session, transaction_manager=tm)
        StrictRedis.from_url.assert_called_with('path/to/redis', decode_responses=True)
        Mailer.from_settings.assert_called_with(settings, "mail.")

        self.assertEqual(site.settings, settings)
        self.assertEqual(site.db_session, db_session)
        self.assertEqual(site.redis, redis)
        self.assertEqual(site.mailer, mailer)
        self.assertEqual(site.transaction_manager, tm)

    def test_from_request(self):
        request = MagicMock()
        site = Site.from_request(request)
        self.assertEqual(site.settings, request.registry.settings)
        self.assertEqual(site.db_session, request.db_session)
        self.assertEqual(site.redis, request.redis)
        self.assertEqual(site.mailer, request.mailer)
        self.assertEqual(site.transaction_manager, request.tm)
