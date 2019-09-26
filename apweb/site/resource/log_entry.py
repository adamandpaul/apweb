# -*- coding:utf-8 -*-

from . import orm
from contextplus import record_property
from contextplus import SQLAlchemyCollection
from contextplus import SQLAlchemyItem
from datetime import datetime
from datetime import timedelta
from uuid import UUID
from uuid import uuid4

import logging


CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10

LEVEL_NAMES = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
}


logger = logging.getLogger("apweb.site.logs")


class LogEntry(SQLAlchemyItem):

    record_type = orm.LogEntry
    id_fields = ("log_entry_id",)
    log_entry_id = record_property("log_entry_id")
    timestamp = record_property("timestamp")
    component = record_property("component")
    level = record_property("level")
    message = record_property("message")

    @property
    def readable_level(self):
        return LEVEL_NAMES.get(self.level, str(self.level))

    @property
    def title(self):
        return f"{self.timestamp}: {self.component}"

    @property
    def description(self):
        return f"{self.readable_level}: {self.message}"


class LogEntryCollection(SQLAlchemyCollection):
    child_type = LogEntry
    default_order_by_fields = ["timestamp desc"]

    def name_from_child(self, child):
        return str(child.log_entry_id)

    def id_from_name(self, name):
        try:
            log_entry_id = UUID(name)
        except ValueError as e:
            raise TypeError("Name is not a valid uuid") from e
        if name != str(log_entry_id):
            raise TypeError("Incorrectly formatted uuid")
        return {"log_entry_id": log_entry_id}

    def iter_recent_logs(self):
        """Return logs within the past day"""
        before = datetime.utcnow() - timedelta(days=1)
        q = self.query()
        q = q.filter(orm.LogEntry.timestamp >= before)
        q = q.order_by(orm.LogEntry.timestamp.desc())
        for record in q:
            yield self.child_from_record(record)


class ComponentLogger(LogEntryCollection):
    """A logger for a component"""

    title = "Logger"

    @property
    def description(self):
        return f'Component logger for component key "{self.component}"'

    def __init__(self, parent=None, name: str = None, component: str = None):
        """Create a component logger"""
        super().__init__(parent=parent, name=name)
        assert isinstance(component, str)
        self.component = component

    def query(self, *args, **kwargs):
        return super().query(*args, **kwargs).filter_by(component=self.component)

    def add(self, level, message):
        """Create a log message"""
        record = orm.LogEntry(
            log_entry_id=uuid4(),
            timestamp=datetime.utcnow(),
            level=level,
            component=self.component,
            message=message,
        )
        self.acquire.db_session.add(record)
        logger.log(level, message)  # Additionally log to the application log

    def debug(self, message):
        """Log an info level message to the log_entry table"""
        self.add(DEBUG, message)

    def info(self, message):
        """Log an info level message to the log_entry table"""
        self.add(INFO, message)

    def warning(self, message):
        """Log an info level message to the log_entry table"""
        self.add(WARNING, message)

    def error(self, message):
        """Log an info level message to the log_entry table"""
        self.add(ERROR, message)

    def critical(self, message):
        """Log an info level message to the log_entry table"""
        self.add(CRITICAL, message)
