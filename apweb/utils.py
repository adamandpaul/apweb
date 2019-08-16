# -*- coding:utf-8 -*-

from numbers import Number


def yesish(value, default=None):
    """Determins if a value is yes"""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, Number):
        return bool(value)
    if isinstance(value, str):
        value = value.strip().lower()
        if value == "":
            return default
        if value in ("y", "yes", "t", "true", "1"):
            return True
        if value in ("n", "no", "f", "false", "0"):
            return False
        raise TypeError("Can not determin a yesish value")
    raise TypeError("Can not determin a yesish value")
