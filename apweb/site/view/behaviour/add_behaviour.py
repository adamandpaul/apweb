# -*- coding:utf-8 -*-


class AddBehaviour(object):
    """Object for addable behaviours"""
    schema_add = None

    def add(self, **kwargs):
        NotImplementedError()
