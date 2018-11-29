# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.user_profile_service import ProfileService
from service.watch_service import WatchService

fans_service = Blueprint('fans_service', __name__)

logger = get_logger('main')

# 关注页关注人
@fans_service.route('/tab/fans/following', methods=['POST'])
def get_watch_users():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data')

    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not user_id or not page_num:
        return handle_param_error()

    service = WatchService()
    try:
        result = service.get_watch(user_id=user_id, page_num=page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|watch video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 关注接口
@fans_service.route('/user/fans/follow', methods=['POST'])
def add_watch():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    command     = data.get("cmd") or ''
    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    status      = data.get("status") or 0

    if not command or not user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.watch(user_id, req_user_id, status)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


#我的粉丝
@fans_service.route('/user/fans/followers', methods=['POST'])
def get_fans():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    command     = data.get("cmd") or ''
    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 0

    if not command or not user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_fans(req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user fans request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

#我关注的人
@fans_service.route('/user/fans/following', methods=['POST'])
def get_watch():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 0

    if not user_id or not req_user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_watch(req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


