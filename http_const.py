#!/home/goedel/python/evtsrc/.env/bin/python
# -*- coding: utf-8 -
#
# This file is part of evtsrc released under the MIT license.
# See the NOTICE for more information.
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
