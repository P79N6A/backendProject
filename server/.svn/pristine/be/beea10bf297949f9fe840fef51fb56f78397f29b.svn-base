# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from service.dance_service import DanceService
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

dance_service = Blueprint('dance_service', __name__)

logger = get_logger('main')

# 获取音乐列表接口
def _list_dance_music(tp=0):
    res  = {'code' : 1000, 'msg' : '成功'}

    service = DanceService()
    try:
        result = service.get_dance_music(tp=tp)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

# 获取音乐列表接口
@dance_service.route('/dance/music/list', methods=['POST'])
def list_dance_music():
    data = request.json
    data = data.get("data")
    if data:
        user_id = data.get("userid") or 0

    return _list_dance_music(tp=1)

# 获取音乐列表接口(按热度)
@dance_service.route('/dance/music/list/hot', methods=['POST'])
def list_dance_music_hot():
    data = request.json
    data = data.get("data")
    if data:
        user_id = data.get("userid") or 0

    return _list_dance_music(tp=1)


#获取某音乐创作的串舞作品列表
def _list_music_works(music_id='', tp=0):
    res  = {'code' : 1000, 'msg' : '成功'}
    service = DanceService()
    try:
        result = service.get_works_by_music_id(music_id=music_id, tp=tp)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

#获取某音乐创作的串舞作品列表
@dance_service.route('/dance/music/works', methods=['POST'])
def list_music_works():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    music_id = data.get("music_id") or 0
    if not music_id:
        return handle_param_error()

    return _list_music_works(music_id=music_id)

#获取某音乐创作的串舞作品列表
@dance_service.route('/dance/music/works/hot', methods=['POST'])
def list_music_works_hot():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    music_id = data.get("music_id") or 0
    if not music_id:
        return handle_param_error()

    return _list_music_works(music_id=music_id, tp=1)

#获取某作品跟舞者列表
def _list_work_dancers(work_id=0, dance_id=0, tp=0, user_id=0):
    res  = {'code' : 1000, 'msg' : '成功'}
    if not (dance_id or work_id):
        return handle_param_error()
    service = DanceService()
    try:
        result = service.get_dancers_by_work_id(work_id=work_id, dance_id=dance_id, tp=tp, user_id=0)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res


#获取某作品跟舞者列表
@dance_service.route('/dance/work/dancers', methods=['POST'])
def list_work_dancers():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0
    work_id = data.get("work_id") or 0
    if not work_id:
        return handle_param_error()

    return _list_work_dancers(work_id=work_id,user_id=user_id)

#获取某作品跟舞者列表
@dance_service.route('/dance/work/dancers/highscore', methods=['POST'])
def list_work_dancers_highscore():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    dance_id = data.get("dance_id") or 0
    #work_id  = data.get("work_id") or 0
    if not dance_id:
        return handle_param_error()

    return _list_work_dancers(dance_id=dance_id, tp=1, user_id=user_id)


#获取某首歌跟舞者列表
@dance_service.route('/dance/music/dancers', methods=['POST'])
def list_music_dancers():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0
    music_id = data.get("music_id") or 0
    if not music_id:
        return handle_param_error()

    service = DanceService()
    try:
        result = service.get_dancers_by_music_id(music_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res


#上报某串舞跟舞者数据
@dance_service.route('/dance/work/dancer/add', methods=['POST'])
def add_work_dancer():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id  = data.get("userid") or 0
    work_id  = data.get("work_id") or 0
    duration = data.get("duration") or 0
    score    = data.get("score") or 0
    #ts       = int(time.time())
    if not user_id or not work_id or not score:
        return handle_param_error()

    service = DanceService()
    try:
        result = service.add_work_dancer(user_id=user_id, work_id=work_id, score=score, duration=duration)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

#获取某首歌跟舞者列表
@dance_service.route('/dance/work/data', methods=['POST'])
def get_work_dance_data():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    user_id = data.get("userid") or 0
    work_id = data.get("work_id") or 0
    if not work_id:
        return handle_param_error()

    service = DanceService()
    try:
        result = service.get_work_data(work_id=work_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

#分享舞蹈成绩
@dance_service.route('/dance/share/grade', methods=['POST'])
def share_dance_grade():
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    data = data.get("data")
    if not data:
        return handle_param_error()

    dance_id = data.get("dance_id") or 0
    if not dance_id:
        return handle_param_error()

    service = DanceService()
    try:
        result = service.share_dance_grade(dance_id=dance_id)
        res    = handle_success(result, 1000, '成功')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        service.close()

    return res

