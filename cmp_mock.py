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


class CmpMock(client.HTTPConnection):
    """
    CmpMock is used to simulate a component communication to an given
    event source allowing to investigating its responses.
    """

    def __init__(self, port: int, timeout: float = 0.01) -> None:
        """
        init sets up a new CmpMock instance to use given port for event
        source request which time out after given timeout.
        """
        super().__init__('localhost', port, timeout)

    def post(self, ep: str = '/', data: dict = None,
             method='POST', headers: dict = None) -> dict:
        """
        post posts to given endpoint ep given data json encoded and
        returns the decoded server response.  Note the method and
        headers arguments are only there to emulate error conditions;
        usually they don't need to be touched.
        """
        headers = headers or {
            http.HDR_CT_JSON.name: http.HDR_CT_JSON.value}
        if data is None:
            self.request(method, ep, body=None, headers=headers)
        else:
            self.request(method, ep, json.dumps(data), headers)
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
                decoded = json.loads(bb.decode())
                decoded['status'] = response.status
                return decoded
        sys.exit(1)
