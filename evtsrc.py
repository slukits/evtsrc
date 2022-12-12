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
posted by a software component to evtsrc's rest api, or if it is
returned from an posted command sequence.  An event source provides the
following API:

    - events/add: to add a new event from a software component to the
      event source

    - events/listen: to register a software component for event
      notification

    - events/api: to register a software component's provided api which
      is used by command sequences

    - events/command: requests the executions of api-calls needed by an
      state changing request.

If software components would communicate to each other as it is typical
for a system of micro services the growth of communication paths in
dependency of the number of components would be exponential.  If a
component only communicates with the event source and the api-provider
the growth would be only linear.  Two other problems are:

    - if components are horizontally scaled it may be that two
      components c and c' receive requests r(c) and r(c') at the time
      the requests are received they may be valid but the execution of
      one of the request may make the other invalid.

    - a request may depend on other components, i.e. an order may need a
      warehouse component to reserve inventory to be accepted.  The
      implementation of commands which is supposed to solve this problem
      leans on the SAGA pattern.  But we not use events to initiate
      operations in an other components since the terminology is
      unsuiting.
"""

from typing import Iterator
from http import HTTPStatus
from collections import namedtuple
import json

import http_const as http


def evtsrc(environ: dict, start_respond: callable) -> Iterator:
    """
    evtsrc is the entry point for the event source server which
    evaluates given wsgi (PEP 3333) environment environ for a mandatory
    json post and leverages start_respond to deliver a mandatory json
    response.
    """
    data = json.dumps({'evtsrc': 'v0.0.0'}).encode('utf-8')
    start_respond(
        http.OK,
        [http.HDR_CT_JSON, http.hdr_content_len(data)]
    )
    return iter([data])
