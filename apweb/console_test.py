# -*- coding:utf-8 -*-

from . import console
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


@patch("configparser.ConfigParser")
@patch("argparse.ArgumentParser")
class TestConsoleMain(TestCase):
    def setUp(self):
        self.site_factory = MagicMock()
        self.cmd_configure = MagicMock()
        self.main = console.Main(self.site_factory, self.cmd_configure)

    def test_arg_parser(self, AP, CP):
        expected = AP.return_value
        result = self.main.arg_parser
        self.assertEqual(result, expected)
        self.cmd_configure.assert_called_with(result.add_subparsers.return_value)

    def test_args(self, AP, CP):
        expected = self.main.arg_parser.parse_args.return_value
        result = self.main.args
        self.assertEqual(result, expected)

    def test_settings(self, AP, CP):
        config_reader = CP.return_value
        expected = config_reader.__getitem__.return_value
        result = self.main.settings
        self.assertEqual(result, expected)
        config_reader.read.assert_called_with(self.main.args.config_file)
        config_reader.__getitem__.assert_called_with("app:main")

    @patch("logging.config.fileConfig")
    def test_call(self, fileConfig, AP, CP):
        self.main()
        fileConfig.assert_called_with(self.main.args.config_file)
        self.main.args.func.assert_called_with(self.main)
