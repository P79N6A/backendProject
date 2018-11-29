# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.video_service import VideoService

video_service = Blueprint('video_service', __name__)

logger = get_logger('main')


# 获取发现视频接口
@video_service.route('/video/discover/list', methods=['POST'])
def get_discover_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''
    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    page_num = data.get("page_num") or 1

    service = VideoService()
    try:
        result = service.get_discover_video(page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|discover video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 内容视频接口
@video_service.route('/video/content/list', methods=['POST'])
def get_content_list():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id    = data.get("userid") or 0
    page_num   = data.get("page_num") or 1
    type_class = data.get("type") or 'all'
    type_id    = data.get("type_id") or 'all'
    tag        = data.get("tag") or 'all'

    service = VideoService()
    try:
        result = service.get_class_video(page_num, type_class, type_id, tag)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|game video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 个人信息串烧视频接口
@video_service.route('/video/user/chuan/list', methods=['POST'])
def get_user_chuan_video():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 1

    if not user_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_chuan_video_by_user(user_id, req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user chuan video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|userc huan video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 获取视频播放url
@video_service.route('/video/url/query', methods=['POST'])
def get_video_url():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0
    vid = data.get("vid") or ''
    game_id = data.get("game_id") or 0

    if not vid:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_url_by_vid(vid=vid,game_id=game_id)
        if not result['url']:
            return handle_param_error()

        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|url query request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 个人信息观看记录接口
@video_service.route('/video/user/see/history', methods=['POST'])
def get_user_see_history():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 1

    if not user_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_user_see_history(user_id, req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|user history video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@video_service.route('/video/share/info', methods=['POST'])
def get_share_video_info():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data') if data else None
    if not data:
        return handle_param_error()

    video_id    = data.get("video_id") or ''
    page_num    = data.get("page_num") or 1

    if not video_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_share_video_info(video_id=video_id, page_num=page_num)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

