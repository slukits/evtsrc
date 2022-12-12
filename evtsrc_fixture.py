#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -
#
# Copyright (c) 2022 Stephan Lukits. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

"""
evtsrc_fixture provides a running event source server in its own
process for testing.
"""

import time
from http import client
from multiprocessing import Process
import random

from gunicorn.app.base import BaseApplication

import http_const as http


# seed to produce with each tests run a different sequence of random
# ports
random.seed()


class EvtsrcFixture(BaseApplication, Process):
    """
    An EvtsrcFixture instance fx spins up an event source server in its
    own process by calling fx.start().  Use fx.terminate() to gracefully
    shut down.
    """

    workers = '1'

    def __init__(self, app) -> None:
        """
        init sets up instantiated event source's host address with a
        random port found in the port property.  I.e. if an event source
        start fails due to port collision an other try will use a
        different port.  The number of workers is set to a minimum, the
        log-level decreased to 'warning' while everything else is left
        to Gunicorn's defaults.
        """
        self.port = random.randrange(49152, 65535)
        self.options = {
            'bind': '127.0.0.1:{}'.format(self.port),
            'workers': EvtsrcFixture.workers,
            'loglevel': 'warning'
        }
        self.application = app
        BaseApplication.__init__(self)
        Process.__init__(self)

    def load_config(self) -> None:
        """
        load_config merges initially set option into gunicorn's
        configuration.
        """
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> None:
        """load provides the entry point to the application."""
        return self.application

    def start(self) -> 'EvtsrcFixture':
        """
        start starts non-blocking an event source server for testing and
        doesn't return before the event source is ready to accept
        requests.
        """
        Process.start(self)
        # don't return from start before the server accepts connections
        retry = 40
        while True:
            time.sleep(0.001)
            try:
                cnn = client.HTTPConnection('localhost', self.port, 0.01)
                headers = {http.HDR_CT_JSON.name: http.HDR_CT_JSON.value}
                response = cnn.request('POST', '/', '', headers)
                # must have read response body to send an other request
                if response:
                    response.read().decode()
            except ConnectionRefusedError:
                retry -= 1
                if retry == 0:
                    raise
            else:
                return self

    def run(self) -> None:
        """run runs the event source app blocking."""
        BaseApplication.run(self)
