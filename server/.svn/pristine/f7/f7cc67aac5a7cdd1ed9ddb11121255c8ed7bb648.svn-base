# -*- coding: UTF-8 -*-
import json
import re

from flask import make_response,send_file
from mimetypes import types_map
from io import BytesIO
#from io import StringIO

def handle_success(data, return_code, msg):
    return handle_response(data, return_code, msg)

def handle_param_error():
    data = {}
    return handle_response(data, 1007, '请求参数错误')

def handle_failure():
    data = {}
    return handle_response(data, 1001, '系统忙，请稍后重试...')

def handle_response(data, return_code, msg):
    result         = {}
    result['code'] = return_code
    result['msg']  = msg
    result['data'] = data

    #logger.info('result => {0}'.format(result))

    text     = json.dumps(dict(result), ensure_ascii = False)
    #length   = len(text.encode('utf-8'))
    response = make_response(text)

    response.headers['Content-Type']   = 'application/json; charset=utf-8'
    #response.headers['Content-Length'] = length
    return response

def make_image_response(image, kind):
    """Creates a cacheable response from given image."""
    mimetype = types_map['.' + kind.lower()]
    io = BytesIO()
    image.save(io, kind.upper())
    io.seek(0)
    return send_file(io, mimetype=mimetype, conditional=True)

def check_param(params):
    if not params:
        return True
    value = params.get("cmd") or None
    if (value is not None and not re.search('^[a-zA-Z_]+$', str(value))):
        return False
    value = params.get("userid") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("duration") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("page_num") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("game_id") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("type") or None
    if (value is not None and not re.search('^[a-zA-Z]+$', str(value))):
        return False
    value = params.get("video_id") or None
    if (value is not None and not re.search('^[a-zA-Z0-9]+$', str(value))):
        return False
    value = params.get("type_id") or None
    if (value is not None and not re.search('^[a-zA-Z0-9]+$', str(value))):
        return False
    value = params.get("tag") or None
    if (value is not None and not re.search('^[a-zA-Z0-9]+$', str(value))):
        return False
    value = params.get("req_user_id") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("status") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("begin_sec") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("begin_usec") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False
    value = params.get("req_user_ids") or None
    if value is not None:
        if not isinstance(value,list) or not len(value):
            return False
        for item in value:
            if not item.has_key("req_user_id") or not re.search('^[0-9]+$', str(item.get("req_user_id"))):
                return False
            if not item.has_key("begin_sec") or not re.search('^[0-9]+$', str(item.get("begin_sec"))):
                return False
            if not item.has_key("begin_usec") or not re.search('^[0-9]+$', str(item.get("begin_usec"))):
                return False
    value = params.get("batch_num") or None
    if (value is not None and not re.search('^[0-9]+$', str(value))):
        return False


    return True

