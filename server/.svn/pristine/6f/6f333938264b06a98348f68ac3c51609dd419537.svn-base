# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.user_profile_service import ProfileService
from service.video_service import VideoService

hotlist_service = Blueprint('hotlist_service', __name__)

logger = get_logger('main')

# 获取达人接口
@hotlist_service.route('/hotlist/master/list', methods=['POST'])
def get_master_list():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''

    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not command or not page_num:
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_master_list(page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|master list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取首页最热视频接口
@hotlist_service.route('/hotlist/video/list', methods=['POST'])
def get_index_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''

    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0

    service = VideoService()
    try:
        result = service.get_hot_video()
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|hot video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res
