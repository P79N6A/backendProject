# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from service.media_service import MediaService
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.video_service import VideoService

third_service = Blueprint('third_service', __name__)

logger = get_logger('main')
@third_service.route('/user/video', methods=['POST'])
def get_user_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    begin_sec   = data.get("begin_sec") or 0
    begin_usec  = data.get("begin_usec") or 0
    batch_num   = data.get("batch_num") or 11

    if not req_user_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_video_by_user(user_id=user_id, req_user_id=req_user_id, begin_sec=begin_sec, begin_usec=begin_usec, batch_num=batch_num)
        if not result:
            return handle_param_error()
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@third_service.route('/watch/video', methods=['POST'])
def get_users_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json


    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id      = data.get("userid") or 0
    req_user_ids = data.get("req_user_ids") or 0
    batch_num    = data.get("batch_num") or 11

    if not user_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_video_by_users(user_id=user_id, req_user_ids=req_user_ids, batch_num=batch_num)
        if not result:
            return handle_param_error()
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

