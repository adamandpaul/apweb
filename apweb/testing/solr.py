# -*- coding:utf-8 -*-

from plone.testing import Layer
import redis
import redis.exceptions
import requests

import time
import os
import os.path
import psycopg2
import shutil
import subprocess
import tempfile


class SolrLayer(Layer):
    """Layer for creating a redis instance"""

    def setUp(self):

        self['solr_home'] = os.environ["SOLR_HOME"]
        self['solr_data'] = None
        self['solr_host'] = 'localhost'
        self['solr_port'] = 48983
        self['solr_url'] = f'http://{self["solr_host"]}:{self["solr_port"]}/'
        self['solr_process'] = None

    def startSolr(self):
        self['solr_data'] = tempfile.mkdtemp()
        args = (
            f'{os.environ["SOLR_PREFIX"]}/bin/solr',
            '-f',
            '-s', self['solr_home'],
            '-t', self['solr_data'],
            '-p', str(self['solr_port']),
            '-h', self['solr_host'],
        )
        self["solr_process"] = subprocess.Popen(
            args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        tries = 0
        while True:
            tries += 1
            try:
                result = requests.get(self['solr_url'])
                assert result.status_code == 200
                break
            except (AssertionError, requests.exceptions.ConnectionError) as e:
                if tries >= 10:
                    raise Exception("Could not connect to solr") from e
                time.sleep(0.4)

    def stopSolr(self):
        # stop redis
        if self["solr_process"]:
            process = self["solr_process"]
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                if self.poll() is None:
                    process.kill()
                    process.wait(timeout=10)

        # remove redis database
        if self["solr_data"] is not None:
            shutil.rmtree(self["solr_data"])
            self['solr_data'] = None

    def testSetUp(self):
        self.startSolr()

    def testTearDown(self):
        self.stopSolr()

    def tearDown(self):
        self.stopSolr()


SOLR_LAYER = SolrLayer()
