# -*- coding:utf-8 -*-

from functools import lru_cache

import argparse
import configparser
import logging
import logging.config


class Main(object):
    def __init__(self, site_factory, cmd_configure):
        self.site_factory = site_factory
        self.cmd_configure = cmd_configure

    @property
    @lru_cache(maxsize=None)
    def arg_parser(self):
        parser = argparse.ArgumentParser(description="console tools")
        parser.add_argument(
            "config_file", help="configuration file to use (e.g. develop.ini)"
        )
        sub_commands = parser.add_subparsers(help="command")
        self.cmd_configure(sub_commands)
        return parser

    @property
    @lru_cache(maxsize=None)
    def args(self):
        return self.arg_parser.parse_args()

    @property
    @lru_cache(maxsize=None)
    def settings(self):
        config_reader = configparser.ConfigParser()
        config_reader.read(self.args.config_file)
        return config_reader["app:main"]

    @property
    @lru_cache(maxsize=None)
    def site(self):
        return self.site_factory(self.settings)

    def __call__(self):

        # Configure logging
        logging.config.fileConfig(self.args.config_file)

        # Execute command
        return self.args.func(self)
