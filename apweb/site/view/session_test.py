# -*- coding:utf-8 -*-

from . import session
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class TestSessionView(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.context = MagicMock()
        self.view = session.SessionView(self.context, self.request)

    @patch('apweb.site.view.session.UserView')
    def test_user(self, UserView):
        self.assertEqual(self.view.user, UserView.return_value.info_manage)
        UserView.assert_called_with(self.request.user, self.request)

    def test_info(self):
        self.view.__dict__['user'] = 'foo'
        self.assertEqual(self.view.info['user'], 'foo')
