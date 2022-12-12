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
returned from a posted command sequence.  An event source provides the
following API:

    - events/add: to add a new event from a software component to the
      event source

    - events/listen: to register a software component for event
      notification

    - events/api: to register a software component's provided api which
      is used by command sequences

    - events/command: requests the executions of api-calls needed for a
      state changing request.

If software components would communicate to each other as it is typical
for a system of micro services the growth of communication paths in
dependency of the number of components would be exponential.  If a
component only communicates with the event source and the api-provider
the growth is constant.  Two other problems are:

    - if components are horizontally scaled it may be that two
      components c and c' receive requests r(c) and r(c') which at the
      time they are received are valid but the execution of one of the
      request may make the other invalid.

    - a request may depend on other components, i.e. an order may need a
      warehouse component to reserve inventory to be accepted.  The
      implementation of commands which is supposed to solve this problem
      leans on the SAGA pattern.  But we not use events to initiate
      operations in other components since the terminology is unsuiting.
"""

from typing import Iterator, Tuple
import json

import http_const as http
import err


def evtsrc(environ: dict, start_respond: callable) -> Iterator:
    """
    evtsrc is the entry point for the event source server which
    evaluates given wsgi (PEP 3333) environment environ for a mandatory
    json post and leverages start_respond to deliver a mandatory json
    response.  

    Note evtsrc_fixture.EvtSrcFixture provides a Gunicorn WSGI HTTP
    server serving this function while cmp_mock.CmpMock emulates a
    software component using a provided event source fixture instance.

    An event source provides its name and version on an empty request:

    >>> fx = EvtsrcFixture(evtsrc).start()
    >>> cmp = CmpMock(fx.port)
    >>> cmp.post()
    {'evtsrc': 'v0.0.0', 'status': 200}

    Note the status value appears in testing only to make things easier.  

    An event source responds a method error if other than post request:

    >>> cmp.post(ep='/test', method='GET')
    {'evtsrc': 'v0.0.0', 'error': 'evtsrc: process POST only', 'status': 405}

    Note the event source fails only if the endpoint is not root.

    An event source responds a request error if content type not json:

    >>> cmp.post(ep='/test', headers={"Content-Type": "text/html"})
    {'evtsrc': 'v0.0.0', 'error': 'evtsrc: expect application/json', 'status': 400}
    >>> fx.terminate()
    """

    if environ[http.ENV_PATH] == '/' or environ[http.ENV_PATH] == '':
        return empty_request(start_respond)

    loc, msg, e = validate(environ)
    if e is not None:
        return e(loc, msg, start_respond)


def empty_request(start_respond: callable) -> bytes:
    data = json.dumps({http.APP_NAME: http.APP_VERSION}).encode('utf-8')
    start_respond(
        http.OK,
        [http.HDR_CT_JSON, http.hdr_content_len(data)]
    )
    return iter([data])


def validate(environ: dict) -> Tuple[str, str, callable]:

    if environ[http.ENV_METHOD] != http.MTH_POST:
        return err.LOC_MAIN, err.MSG_POST_ONLY, err.method

    if environ.get(http.HDR_CT_JSON.name) != http.HDR_CT_JSON.value:
        return err.LOC_MAIN, err.MSG_CONTENT_TYPE, err.content_type

    return "", "", None


if __name__ == "__main__":
    from evtsrc_fixture import EvtsrcFixture
    from cmp_mock import CmpMock
    import doctest
    doctest.testmod()
