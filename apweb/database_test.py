# -*- coding: utf-8 -*-

from . import database
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import pyramid.events


class TestDatabaseConfiguration(TestCase):
    @patch("zope.sqlalchemy.register")
    def test_db_session_from_request(self, zope_register):
        request = MagicMock()
        expected_db_session = request.registry["db_session_factory"].return_value
        database.db_session_from_request(request)
        zope_register.assert_called_with(
            expected_db_session, transaction_manager=request.tm
        )

    @patch("sqlalchemy.orm.configure_mappers")
    def test_run_orm_configure_mappers(self, configure_mappers):
        database.run_orm_configure_mappers(None)
        configure_mappers.assert_called_with()

    @patch("sqlalchemy.engine_from_config")
    @patch("sqlalchemy.orm.sessionmaker")
    def test_includeme(self, sessionmaker, engine_from_config):
        config = MagicMock()
        config.registry = {}
        database.includeme(config)
        engine_from_config.assert_called_with(
            config.get_settings.return_value, "sqlalchemy."
        )
        db_engine = engine_from_config.return_value
        db_session_factory = sessionmaker.return_value
        db_session_factory.configure.assert_called_with(bind=db_engine)
        self.assertEqual(config.registry["db_engine"], db_engine)
        self.assertEqual(config.registry["db_session_factory"], db_session_factory)
        config.add_subscriber.assert_called_with(
            database.run_orm_configure_mappers, pyramid.events.ApplicationCreated
        )
