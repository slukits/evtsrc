#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -
#
# Copyright (c) 2022 Stephan Lukits. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

"""
cmp_mock mocks up a software component which together with an event
source fixture allows for end to end tests.  I.e. it provides an http
client posting requests against an event source's rest API and processes
its json responses.
"""


import sys
from typing import Any
from http import client
import json

import http_const as http
from evtsrc_fixture import EvtsrcFixture


class CmpMock(client.HTTPConnection):
    """
    CmpMock is used to simulate a component communication to an given event
    source allowing to investigating its responses.
    """

    def __init__(self, port: int, timeout: float = 0.01) -> None:
        """
        init sets up a new CmpMock instance to use given port for event
        source request which time out after given timeout.
        """
        timeout = timeout or 0.01
        super().__init__('localhost', port, timeout)

    def post(self, ep: str = None, data: dict = None) -> dict:
        """
        post posts to given endpoint ep given data json encoded
        and returns the decoded server response.
        """
        ep, data = ep or '/', data or {}
        headers = {http.HDR_CT_JSON.name: http.HDR_CT_JSON.value}
        self.request('POST', ep, json.dumps(data), headers)
        try:
            response = self.getresponse()
        except ConnectionError:
            print >> sys.stderr,
            "component mock: post: couldn't connect to event source"
        except client.ResponseNotReady:
            print >> sys.stderr,
            "component mock: post: couldn't retrieve from event source"
        else:
            try:
                bb = response.read()  # type: bytes
            except client.IncompleteRead:
                print >> sys.stderr,
                "component mock: post: couldn't finish read from evtsrc"
            else:
                return json.loads(bb.decode())
        sys.exit(1)


if __name__ == '__main__':
    fx = EvtsrcFixture()
    fx.start()
    print(CmpMock(fx.port).post())
    fx.terminate()
