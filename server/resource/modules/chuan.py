# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param
from service.history_service import HistoryService
from service.chuan import ChuanService

chuan_service = Blueprint('chuan_service', __name__)

logger = get_logger('main')

# 获取观看记录
@chuan_service.route('/chuan/video/history/query', methods=['POST'])
def chuan_video_query():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()


    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = HistoryService()
    try:
        result = service.get_chuan_history(user_id=user_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|chuan history query list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


#查询名字
@chuan_service.route('/chuan/title/query', methods=['POST'])
def query_chuan_job_title():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    uid  = data.get('userid') or 0
    #duration  = data.get('data').get('duration') or 0
    vids = data.get('video_ids') or []
    if not (uid and vids and len(vids)):
        logger.error('fail|userid or vid is null, return')
        return handle_param_error()

    s = ChuanService()
    try:
        result = s.query_title(uid=uid, vids=vids)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error('fail|exception|chuan/title/query request serve error|%s' % traceback.format_exc())
    finally:
        s.close()

    return res

