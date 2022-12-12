#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Stephan Lukits. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

"""
evtsrc is an event source storing a software system's state changing
events and broadcasts them to event listeners respectively provides them
to client request.  An event becomes part of an event source if it is
posted by a software component to evtsrc's rest api, or if it is emitted
by an event-generator which is posted to an event source by a software
component.
"""

from http import HTTPStatus
from collections import namedtuple
import json

OK = "{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
BAD = "{} {}".format(
    HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)

hdr = namedtuple('hdr', 'name value')
HDR_CT_JSON = hdr("Content-Type", "application/json")


def hdr_content_len(data): return hdr("Content-Length", str(len(data)))


def evtsrc(environ, start_respond):
    """evtsrc is the entry point for the event source server which
    evaluates given wsgi (PEP 3333) environment environ for a mandatory
    json post and leverages start_respond to deliver a mandatory json
    response.
    """
    data = json.dumps({'evtsrc': 'v0.0.0'}).encode('utf-8')
    start_respond(OK, [HDR_CT_JSON, hdr_content_len(data)])
    return iter([data])
