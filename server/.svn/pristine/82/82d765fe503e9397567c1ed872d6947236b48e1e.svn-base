# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from service.media_service import MediaService
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

medias_service = Blueprint('medias_service', __name__)

logger = get_logger('main')
# 获取音乐列表接口
@medias_service.route('/music/list', methods=['POST'])
def list_music():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data    = data.get("data")
    if data:
        user_id = data.get("userid") or 0

    service = MediaService()
    try:
        result = service.get_music(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|music list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@medias_service.route('/user/video/chuanwu', methods=['POST'])
def list_user_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = MediaService()
    try:
        result = service.get_video(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@medias_service.route('/user/picture/wall', methods=['POST'])
def list_user_picture():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = MediaService()
    try:
        result = service.get_picture(user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user picture list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

