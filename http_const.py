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

from typing import Tuple
from http import HTTPStatus
from collections import namedtuple

OK = "{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
ERR_BAD = "{} {}".format(
    HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
ERR_MTH = "{} {}".format(
    HTTPStatus.METHOD_NOT_ALLOWED.value,
    HTTPStatus.METHOD_NOT_ALLOWED.phrase
)

hdr = namedtuple('hdr', 'name value')
HDR_CT_JSON = hdr("Content-Type", "application/json")


def hdr_content_len(data) -> Tuple[str, str]:
    return hdr("Content-Length", str(len(data)))


APP_NAME = 'evtsrc'
APP_VERSION = 'v0.0.0'

ENV_METHOD = 'REQUEST_METHOD'
MTH_POST = 'POST'

ENV_PATH = 'PATH_INFO'
