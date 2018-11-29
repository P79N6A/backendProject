# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request
from service.qrcode_service import QRCodeService
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param,make_image_response

qrcode_service = Blueprint('qrcode_service', __name__)

logger = get_logger('main')

##获取某首歌跟舞者列表
#@qrcode_service.route('/qrcode/share/video', methods=['POST','GET'])
#def get_share_video():
#    data = request.json
#
#    data = data.get("data") if data else None
#    if data:
#        user_id  = data.get("userid") or 0
#        video_id = data.get("video_id") or ''
#
#    user_id  = request.args.get('userid')
#    video_id = request.args.get('video_id')
#
#    if not user_id or not video_id:
#        return handle_param_error()
#
#    service = QRCodeService()
#    try:
#        image = service.get_share_video_image(user_id=user_id, video_id=video_id)
#        res   = make_image_response(image, 'png')
#    except:
#        res = handle_failure()
#        logger.error(traceback.format_exc())
#    finally:
#        pass
#
#    return res

#获取个人信息页
@qrcode_service.route('/qrcode/profile/edit', methods=['POST','GET'])
def edit_profile_info():
    data = request.json

    data = data.get("data") if data else None
    if data:
        user_id  = data.get("userid") or 0
    else:
        user_id  = request.args.get('userid')

    if not user_id:
        return handle_param_error()

    service = QRCodeService()
    try:
        image = service.get_profile_info_image(user_id=user_id)
        res   = make_image_response(image, 'png')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        pass

    return res

#获取跳舞成绩
@qrcode_service.route('/qrcode/dance/grade', methods=['POST','GET'])
def get_dance_grade():
    data = request.json

    data = data.get("data") if data else None
    if data:
        dance_id  = data.get("dance_id") or 0
    else:
        dance_id  = request.args.get('dance_id')

    if not dance_id:
        return handle_param_error()

    service = QRCodeService()
    try:
        image = service.get_dance_grade_image(dance_id=dance_id)
        res   = make_image_response(image, 'png')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        pass

    return res

#分享视频
@qrcode_service.route('/qrcode/video/share', methods=['POST','GET'])
def share_video():
    data = request.json

    data = data.get("data") if data else None
    if data:
        video_id  = data.get("video_id") or 0
    else:
        video_id  = request.args.get('video_id')

    if not video_id:
        return handle_param_error()

    service = QRCodeService()
    try:
        image = service.get_video_image(video_id=video_id)
        res   = make_image_response(image, 'png')
    except:
        res = handle_failure()
        logger.error(traceback.format_exc())
    finally:
        pass

    return res
