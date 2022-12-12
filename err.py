# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Stephan Lukits. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import json
import http_const as http

LOC_MAIN = http.APP_NAME

MSG_POST_ONLY = 'process POST only'
MSG_CONTENT_TYPE = 'expect application/json'


def method(loc: str, msg: str, start_respond: callable):
    # jsn = _err_json(loc, msg)  # type: bytes
    jsn = json.dumps({
        http.APP_NAME: http.APP_VERSION,
        'error': '{}: {}'.format(loc, msg)
    }).encode('utf-8')
    start_respond(
        http.ERR_MTH,
        [http.HDR_CT_JSON, http.hdr_content_len(jsn)]
    )
    return iter([jsn])


def content_type(loc: str, msg: str, start_respond: callable):
    # jsn = _err_json(loc, msg)  # type: bytes
    jsn = json.dumps({
        http.APP_NAME: http.APP_VERSION,
        'error': '{}: {}'.format(loc, msg)
    }).encode('utf-8')
    start_respond(
        http.ERR_BAD,
        [http.HDR_CT_JSON, http.hdr_content_len(jsn)]
    )
    return iter([jsn])


def _err_json(loc: str, msg: str) -> bytes:
    return json.dumps({
        http.APP_NAME: http.APP_VERSION,
        'error': '{}: {}'.format(loc, msg)
    }).encode('utf-8')
