#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -
#
# This file is part of evtsrc released under the MIT license.
# See the NOTICE for more information.
"""
evtsrc_fixture provides a running event source server in its own
process for testing.
"""

import time
from http import client
from multiprocessing import Process

from gunicorn.app.base import BaseApplication

from evtsrc import evtsrc
import http_const as http


class EvtsrcFixture(BaseApplication, Process):
    """
    An EvtsrcFixture instance fx spins up an event source server in its
    own process by calling fx.start().  Use fx.post-method to post to
    its rest-api.
    """

    # port allows us to spin up for each test case an event source
    # server with different port in case the os hasn't released a port
    # between to test cases.
    port = 11000

    workers = '1'

    def __init__(self):
        self.port = EvtsrcFixture.port + 1
        self.options = {
            'bind': '127.0.0.1:{}'.format(self.port),
            'workers': EvtsrcFixture.workers,
        }
        self.application = evtsrc
        BaseApplication.__init__(self)
        Process.__init__(self)

    def load_config(self):
        """
        load_config merges initially given option into gunicorn's
        configuration.
        """
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """load provides the entry point to the application."""
        return self.application

    def start(self):
        Process.start(self)
        # don't return from start before the server accepts connections
        retry = 20
        while True:
            time.sleep(0.002)
            try:
                cnn = client.HTTPConnection('localhost', 11001, 0.01)
            except ConnectionRefusedError:
                retry -= 1
                if retry == 0:
                    raise
            else:
                break

    def run(self):
        """run spins up the event source server fixture for testing."""
        BaseApplication.run(self)


if __name__ == "__main__":
    fx = EvtsrcFixture()
    fx.start()
    fx.join()
