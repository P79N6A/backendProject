# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.user_profile_service import ProfileService

profile_service = Blueprint('profile_service', __name__)

logger = get_logger('main')

# 上报失效头像
@profile_service.route('/user/profile/invalid/icon', methods=['POST'])
def update_invalid_icon():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.add_invalid_icon(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user profile request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取个人信息接口
@profile_service.route('/user/profile/info/userid', methods=['POST'])
def get_user_profile_by_id():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_user_profile_by_id(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user profile request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 获取个人信息接口
@profile_service.route('/user/profile/info', methods=['POST'])
def get_user_profile():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_user_profile(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user profile request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 更新个人信息接口
@profile_service.route('/user/profile/update', methods=['POST'])
def update_user_profile():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id   = data.get("userid") or 0
    signature = data.get("signature") or ''
    nickname  = data.get("nickname") or ''
    user_icon = data.get("user_icon") or ''
    user_pics = data.get("user_pics") or []

    if not user_id or not nickname or not user_icon:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.update_user_profile_diy(user_id=user_id, signature=signature,
                                                 nickname=nickname, user_icon=user_icon,
                                                 user_pics=user_pics)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user profile request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@profile_service.route('/user/profile/iswatch', methods=['POST'])
def is_watch():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0

    if not user_id or not req_user_id:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.user_watch_relation(user_id, req_user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|is watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

