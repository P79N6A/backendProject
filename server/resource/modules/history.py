# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,check_param
from service.history_service import HistoryService

history_service = Blueprint('history_service', __name__)

logger = get_logger('main')

#视频观看记录
@history_service.route('/history/video/add', methods=['POST'])
def add_history():
    res = {'code':1000,'msg':'success'}
    data = request.json

    data = data.get('data')
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    video_id = data.get("video_id") or ''
    duration = data.get("duration") or 0

    if not (user_id and video_id):
        return handle_param_error()

    service = HistoryService()

    try:
        result = service.add_history(user_id=user_id, video_id=video_id, duration=duration)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|add history request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


