#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -
#
# Copyright (c) 2022 Stephan Lukits. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

"""
http const provides mainly http header constants in a broader sense
needed by evtsrc, cmp_mock and evtsrc_fixture modules.
"""

from http import HTTPStatus
from collections import namedtuple

OK = "{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
BAD = "{} {}".format(
    HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)

hdr = namedtuple('hdr', 'name value')
HDR_CT_JSON = hdr("Content-Type", "application/json")


def hdr_content_len(data): return hdr("Content-Length", str(len(data)))
