# -*- coding:utf-8 -*-

from . import log_entry
from . import orm
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID


class TestLogEntry(TestCase):
    def setUp(self):
        self.record = orm.LogEntry(
            log_entry_id=UUID("089d78b2-a55c-485e-9df6-a8ad5f16b991"),
            timestamp=datetime(2000, 1, 2),
            component="widget",
            level=20,
            message="Hi",
        )
        self.entry = log_entry.LogEntry(record=self.record)

    def test_properties(self):
        e = self.entry
        self.assertEqual(e.log_entry_id, UUID("089d78b2-a55c-485e-9df6-a8ad5f16b991"))
        self.assertEqual(e.readable_level, "INFO")
        self.assertEqual(e.title, "2000-01-02 00:00:00: widget")
        self.assertEqual(e.description, "INFO: Hi")


class TestLogEntryCollection(TestCase):
    def setUp(self):
        self.collection = log_entry.LogEntryCollection()

    def test_name_from_child(self):
        child = MagicMock()
        child.log_entry_id = UUID("089d78b2-a55c-485e-9df6-a8ad5f16b991")
        result = self.collection.name_from_child(child)
        self.assertEqual(result, "089d78b2-a55c-485e-9df6-a8ad5f16b991")

    def test_id_from_name(self):
        result = self.collection.id_from_name("089d78b2-a55c-485e-9df6-a8ad5f16b991")
        self.assertEqual(
            result, {"log_entry_id": UUID("089d78b2-a55c-485e-9df6-a8ad5f16b991")}
        )

    def test_iter_recent_logs(self):
        self.collection.query = MagicMock()
        self.collection.child_from_record = MagicMock()
        qresults = ["foo", "bar"]
        self.collection.query.return_value.filter.return_value.order_by.return_value = (
            qresults
        )
        results = list(self.collection.iter_recent_logs())
        self.collection.child_from_record.assert_any_call("foo")
        self.collection.child_from_record.assert_any_call("bar")
        self.assertEqual(len(results), 2)


class TestComponentLogger(TestCase):
    def setUp(self):
        self.logger = log_entry.ComponentLogger(component="user")
        self.logger.db_session = MagicMock()

    @patch("apweb.site.resource.log_entry.datetime")
    @patch("apweb.site.resource.log_entry.uuid4")
    @patch("apweb.site.resource.orm.LogEntry")
    def test_add(self, LogEntry, uuid4, datetime):
        self.logger.add(44, "Hello")
        LogEntry.assert_called_with(
            log_entry_id=uuid4.return_value,
            timestamp=datetime.utcnow.return_value,
            level=44,
            component="user",
            message="Hello",
        )
        self.logger.db_session.add.assert_called_with(LogEntry.return_value)
