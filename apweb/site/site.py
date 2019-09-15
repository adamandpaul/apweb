# -*- coding:utf-8 -*-

import contextplus


class Site(contextplus.Site):
    """A primitive site"""

    def __init__(self, *args, mailer=None, transaction_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailer = mailer
        self.transaction_manager = transaction_manager
