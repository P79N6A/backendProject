# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request,render_template,url_for,redirect
from lib.log import get_logger
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

h5_service = Blueprint('h5_service', __name__, static_folder='static')

logger = get_logger('main')

#获取某首歌跟舞者列表
@h5_service.route('/h5/share/video', methods=['GET'])
def get_share_video_page():
    user_id  = request.args.get('userid')
    video_id = request.args.get('video_id')
    if not user_id or not video_id:
        return handle_param_error()

    return render_template('index.html', user_id=user_id, video_id=video_id)

#获取某首歌跟舞者列表
@h5_service.route('/h5/profile/edit', methods=['GET'])
def edit_ht_profile():
    user_id  = request.args.get('userid')
    if not user_id:
        return handle_param_error()

    return redirect('%s?%s'%(url_for('static', filename='edit.html'),'userid=%s'%user_id))

    #return render_template('/edit/edit.html', userid=userid)

#分享视频
@h5_service.route('/h5/video/share', methods=['GET'])
def share_video():
    video_id  = request.args.get('video_id')
    if not video_id:
        return handle_param_error()

    return redirect('%s?%s'%(url_for('static', filename='game.html'),'video_id=%s'%video_id))

#分享跳舞成绩
@h5_service.route('/h5/dance/grade', methods=['GET'])
def share_dance_grade():
    dance_id  = request.args.get('dance_id')
    if not dance_id:
        return handle_param_error()

    return redirect('%s?%s'%(url_for('static', filename='dance.html'),'dance_id=%s'%dance_id))

