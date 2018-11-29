# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from service.notice_service import NoticeService
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

notice_service = Blueprint('notice_service', __name__)

logger = get_logger('main')

#获取闪屏通知
@notice_service.route('/notice/query/main', methods=['POST'])
def get_main_notice():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0
    ts      = data.get("timestamp") or 0
    service = NoticeService()
    try:
        result = service.get_main_notice(user_id=user_id, timestamp=ts)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res
