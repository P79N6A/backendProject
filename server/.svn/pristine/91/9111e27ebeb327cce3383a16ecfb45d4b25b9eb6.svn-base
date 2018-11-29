# -*- coding: UTF-8 -*-
from flask import Flask,jsonify,request,redirect
from dao.page_content import PageContent
from dao.user_video import UserVideo
from dao.video import Video
from dao.base import BaseDao
from dao.user_behavior import UserBehavior
from lib.log import get_logger
from lib.tool import validSqlInject
from dao.user import User
from dao.billboard import Billboard
from lib.tool import get_user_id
from service.comment_service import CommentService
from service.video_service import VideoService
from service.version_service import VersionService
from service.docker_name_service import DockerRouter
from service.user_profile_service import ProfileService
from service.category_service import CategoryService
from service.tag_service import TagService
from service.history_service import HistoryService
from service.chuan import ChuanService
from service.watch_service import WatchService

from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

#routers
from modules.medias import medias_service
from modules.login  import login_service
from modules.third_res  import third_service

import sys
#import logging
import traceback
import time
import urllib
import zerorpc
#import json
#from flask import make_response
#import re


logger = get_logger('main')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#register routers
app.register_blueprint(medias_service)
app.register_blueprint(login_service)
app.register_blueprint(third_service)

reload(sys)
sys.setdefaultencoding('utf-8')


@app.route('/ub', methods=['GET', 'POST'])
def ub():
    logger.info('rec a ub request')
    data = request.json
    uid = data.get('userid')
    vid = data.get('id')
    if validSqlInject(vid) or validSqlInject(uid):
        return jsonify({'code':1, 'msg':'invalid param'})
    if not (uid and vid):
        logger.info('fail|userid or vid is null, return')
        return jsonify({'code':-1, 'msg':'need userid and vid'})
    if len(uid) > 32 or len(vid) > 32:
        logger.info('fail|userid or vid is invalid,userid:%s,vid:%s return' %(uid, vid))
        return jsonify({'code':-1, 'msg':'userid and vid invalid.'})
    duration = data.get('duration') or 0

    b = BaseDao()
    try:
        uv = UserVideo(base=b)
        v_dao = Video(base=b)
        uv.add_item(uid, vid, int(time.time()), duration)
        v_dao.add_play_count(vid)
        logger.info('success|ub request serve success')
    except:
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    return jsonify({'code':0, 'msg':'success'})

@app.route('/uid')
def uid():
    logger.info('rec a uid request')
    res = {'code':1,'msg':'success', 'uid':'unkown'}

    b = BaseDao()
    try:
        user_dao = User(base=b)
        macid = request.args.get("macid") or ''
        androidid = request.args.get("androidid") or ''
        if validSqlInject(macid) or validSqlInject(androidid):
            return jsonify({'code':1, 'msg':'invalid param'})

        if macid or androidid:
            user = user_dao.get_user_info(macid, androidid)
            if not user:
                uid = get_user_id(macid, androidid)
                user_dao.add_user_id(uid, macid, androidid)
            else:
                uid = user.user_id

            res['uid'] = uid
        else:
            res['uid'] = get_user_id()

        logger.info('success|uid request serve success')
    except:
        logger.error('fail|exception|uid request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    return jsonify(res)

@app.route('/billboard', methods=['GET'])
def billboard():
    logger.info('rec a billboard request')
    res = {'code':1,'msg':'success', 'qr':'', 'notice':''}

    b = BaseDao()
    try:
        bb_dao = Billboard(base=b)
        bb = bb_dao.get_billboard_info()
        logger.info('success|billboard request serve success')
    except:
        logger.error('fail|exception|billboard request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    res['qr'] = bb.qr_url
    res['notice'] = bb.notice
    return jsonify(res)

@app.route('/history', methods=['GET'])
def history():
    logger.info('rec a history request')
    res = {'code':1,'msg':'success', 'content':{}}
    userid = request.args.get("userid") or ''
    if not userid:
        res['code'] = 0
        res['msg']  = 'need userid'
        return jsonify(res)
    if validSqlInject(userid):
        return jsonify({'code':1, 'msg':'invalid param'})

    if len(userid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    content = {}
    itemList = []
    content['itemList'] = itemList
    b = BaseDao()
    try:
        ub = UserBehavior(userid, b)
        for v_obj in ub.get_video_items():
            #v_obj = assemble(item)
            itemList.append(v_obj)

        res['content'] = content
        logger.info('success|history request serve success')
    except:
        logger.error('fail|exception|history request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    return jsonify(res)

@app.route('/delhistory', methods=['GET'])
def del_history():
    logger.info('rec a delhistory request')
    res = {'code':1,'msg':'success'}
    userid = request.args.get("userid") or ''
    vid = request.args.get("vid") or ''
    if not (userid and vid):
        res['code'] = 0
        res['msg']  = 'need userid and vid'
        return jsonify(res)
    if len(userid) > 32 or len(vid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    b = BaseDao()
    ub = UserBehavior(userid, b)
    try:
        ub.del_video_history(vid)
        logger.info('success|delhistory request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|delhistory request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    return jsonify(res)

@app.route('/delallhistory', methods=['GET'])
def del_all_history():
    logger.info('rec a delallhistory request')
    res = {'code':1,'msg':'success'}
    userid = request.args.get("userid") or ''
    if not userid:
        res['code'] = 0
        res['msg']  = 'need userid'
        return jsonify(res)
    if len(userid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    b = BaseDao()
    ub = UserBehavior(userid, b)
    try:
        ub.del_all_video_history()
        logger.info('success|delallhistory request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|delallhistory request serve error|%s' % traceback.format_exc())
    finally:
        b.close()

    return jsonify(res)

# 获取评论配置接口
@app.route('/list/comment', methods=['POST'])
def list_comment():
    logger.info('rec a list_comment request')
    res    = {'code' : 0, 'msg' : 'success', 'list' : ''}
    data   = request.json
    if not check_param(data):
        return handle_param_error()

    userid = data.get("userid") or ''
    if not userid:
        res['code'] = -1
        res['msg']  = 'need userid'
        return jsonify(res)
    if len(userid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    service = CommentService()
    try:
        result      = service.get_base_comment()
        res['list'] = result
        logger.info('success|list_comment request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|list_comment request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return jsonify(res)

# 评论视频接口
@app.route('/user/add/video/comment', methods=['POST'])
def add_comment():
    logger.info('rec a add_comment request')
    res          = {'code' : 0, 'msg' : 'success'}
    data         = request.json
    if not check_param(data):
        return handle_param_error()

    vid          = data.get("vid") or ''
    content      = data.get("content") or ''
    userid       = data.get("userid") or ''
    uname        = data.get("uname") or ''
    comment_time = data.get("comment_time") or ''

    if not userid or not vid or not comment_time or not content:
        res['code'] = -1
        res['msg']  = 'need userid、vid、comment time、comment content'
        return jsonify(res)
    if len(userid) > 32 or len(vid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    service = CommentService()
    try:
        service.add_video_comment(vid, content, userid, comment_time, uname)
        logger.info('success|add_comment request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|add_comment request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return jsonify(res)

# 弹幕接口
@app.route('/user/display/video/comment', methods=['POST'])
def display_comment():
    logger.info('rec a display_comment request')
    res    = {'code' : 0, 'msg' : 'success', 'xml': ''}
    data   = request.json
    if not check_param(data):
        return handle_param_error()

    vid    = data.get("vid") or ''
    userid = data.get("userid") or ''

    if not userid or not vid:
        res['code'] = 1
        res['msg']  = 'need userid、vid'
        return jsonify(res)

    if len(userid) > 32 or len(vid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    service = CommentService()
    try:
        xml = service.get_video_comment(vid)
        if (xml == ''):
            res['code'] = 1
            res['msg']  = '该视频不存在评论'
        else:
            res['xml'] = xml
        logger.info('success|display_comment request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|display_comment request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return jsonify(res)


# 点赞接口
@app.route('/user/praise/video', methods=['POST'])
def user_praise():
    logger.info('rec a user_praise request')
    res    = {'code' : 0, 'msg' : 'success'}
    data   = request.json
    if not check_param(data):
        return handle_param_error()

    vid    = data.get("vid") or ''
    userid = data.get("userid") or ''

    if not userid or not vid:
        res['code'] = 1
        res['msg']  = 'need userid、vid'
        return jsonify(res)
    if len(userid) > 32 or len(vid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    service = VideoService()
    try:
        service.add_video_good(vid)
        logger.info('success|user_praise request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|user_praise request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return jsonify(res)

# 版本更新接口
@app.route('/version/update', methods=['POST'])
def version_update():
    logger.info('rec a version_update request')
    res          = {'code' : 0, 'msg' : 'success', 'url': '', 'force': 0}
    data         = request.json
    if not check_param(data):
        return handle_param_error()

    userid       = data.get("userid") or ''
    version_code = data.get("version_code") or 0

    if not userid or version_code == 0:
        res['code'] = 1
        res['msg']  = 'need userid and version code'
        return jsonify(res)

    if len(userid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    service = VersionService()
    try:
        (res['url'], res['force']) = service.get_update(version_code)
        logger.info('success|version_update request serve success')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|version_update request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return jsonify(res)

# 语音转文字接口代理
@app.route('/voice/request/to/text', methods=['POST'])
def voice_to_text():
    logger.info('rec a voice convert text request')
    res        = {'code' : 0, 'msg' : 'success'}
    data       = request.json
    if not check_param(data):
        return handle_param_error()

    userid     = data.get("userid") or ''
    voice_data = data.get("voice_data") or ''

    if not userid or not voice_data:
        res['code'] = 1
        res['msg']  = 'need userid and voice data'
        return jsonify(res)

    if len(userid) > 32:
        logger.info('fail|user arg invalid, return')
        return jsonify({'code':-1, 'msg':'userid invalid'})

    client = zerorpc.Client()
    try:
        router     = DockerRouter()
        (ip, port) = router.get_router('Voice', 'VoiceService')
        client.connect('tcp://{0}:{1}'.format(ip, port))
        if (client.sng_voice(voice_data) == True):
            logger.info('success|voice to text request success')
        else:
            res['code'] = 1
            res['msg']  = '操作失败'
            logger.info('failure|voice to text request failure')
    except:
        res['code'] = 1
        res['msg']  = '操作失败'
        logger.error('fail|exception|voice to text request serve error|%s' % traceback.format_exc())
    finally:
        client.close()

    return jsonify(res)

# 语音转文字腾讯云回调地址代理
# 这个接口和腾讯云语音识别有关，因此里面的返回信息和自身业务有区别
@app.route('/voice/callback', methods=['POST'])
def voice_callback():
    logger.info('rec a voice convert text callback request')
    res        = {'code' : 0, 'message' : 'success'}

    logger.info('form data => {0}'.format(request.form))

    return_code = int(request.form.get('code', 1))
    message     = urllib.unquote(request.form.get('message', 'defaule value'))
    requestId   = request.form.get('requestId', 0)
    appid       = request.form.get('appid', 0)
    projecteid  = request.form.get('projecteid', 0)
    text        = urllib.unquote(request.form.get('text', 'defaule value'))
    audioTime   = request.form.get('audioTime', 0)

    client = zerorpc.Client()
    try:
        router     = DockerRouter()
        (ip, port) = router.get_router('Voice', 'VoiceService')
        client.connect('tcp://{0}:{1}'.format(ip, port))
        if (return_code == 0 and client.sng_voice_callback(requestId, text, audioTime) == True):
            logger.info('success|voice to text callback success')
        else:
            res['code']     = 1
            res['message']  = '操作失败'
            logger.info('failure|voice to text callback failure')
    except:
        res['code']     = 1
        res['message']  = '操作失败'
        logger.error('fail|exception|voice to text callback serve error|%s' % traceback.format_exc())
    finally:
        client.close()

    return jsonify(res)


# 获取个人信息接口
@app.route('/user/profile/get', methods=['POST'])
def get_user_profile():
    logger.info('rec a user profile get request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command = data.get("cmd") or ''

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id = data.get("userid") or 0

    if not command or not user_id or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_user_profile(user_id)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user profile request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|user profile request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取达人接口
@app.route('/user/master/list', methods=['POST'])
def get_master_list():
    logger.info('rec a master list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()


    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not command or not page_num or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_master_list(page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|master list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|master list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取首页最热视频接口
@app.route('/video/hot/list', methods=['POST'])
def get_index_video():
    logger.info('rec a hot video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id  = data.get("userid") or 0

    if not command or not check_param(data):
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_hot_video()
        res    = handle_success(result, 1000, '成功')
        logger.info('success|hot video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|hot video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取发现视频接口
@app.route('/video/discover/list', methods=['POST'])
def get_discover_video():
    logger.info('rec a discover video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not command or not page_num or not check_param(data):
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_discover_video(page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|discover video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|discover video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 导航接口
@app.route('/category/list', methods=['POST'])
def list_category():
    logger.info('rec a category list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command  = data.get("cmd") or ''

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id  = data.get("userid") or 0

    if not command or not check_param(data):
        return handle_param_error()

    service = CategoryService()
    try:
        result = service.get_categorys()
        res    = handle_success(result, 1000, '成功')
        logger.info('success|category request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|category request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 关注页关注人
@app.route('/video/watch/users', methods=['POST'])
def get_watch_users():
    logger.info('rec a watch video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()


    #command  = data.get("cmd") or ''
    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not user_id or not page_num or not check_param(data):
        return handle_param_error()

    service = WatchService()
    try:
        result = service.get_watch(user_id=user_id, page_num=page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|watch video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|watch video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 关注页视频接口
@app.route('/video/watch/videos', methods=['POST'])
def get_watch_videos():
    logger.info('rec a watch video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not user_id or not page_num or not check_param(data):
        return handle_param_error()

    service = WatchService()
    try:
        result = service.get_watch_videos(user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|watch video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|watch video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


# 关注页接口
@app.route('/video/watch/list', methods=['POST'])
def get_watch_list():
    logger.info('rec a watch video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id  = data.get("userid") or 0
    page_num = data.get("page_num") or 1

    if not user_id or not page_num or not check_param(data):
        return handle_param_error()

    service = WatchService()
    try:
        result = service.get_watch_video(user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|watch video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|watch video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 内容视频接口
@app.route('/video/content/list', methods=['POST'])
def get_content_list():
    logger.info('rec a game video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    command    = data.get("cmd") or ''
    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id    = data.get("userid") or 0
    page_num   = data.get("page_num") or 1
    type_class = data.get("type") or 'all'
    type_id    = data.get("type_id") or 'all'
    tag        = data.get("tag") or 'all'

    if not command or not page_num or not check_param(data):
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_class_video(page_num, type_class, type_id, tag)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|game video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|game video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 拉取游戏的标签
@app.route('/tags/content/list', methods=['POST'])
def get_tags():
    logger.info('rec a tag list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command    = data.get("cmd") or ''

    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id    = data.get("userid") or 0
    type_id    = data.get("type_id") or 'all'

    if not command or not type_id or not check_param(data):
        return handle_param_error()

    service = TagService()
    try:
        result = service.get_tag_by_content(type_id)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|tag list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|tag list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 个人信息视频接口
#@app.route('/video/user/list', methods=['POST'])
#def get_user_video():
#    logger.info('rec a user video list request')
#    res  = {'code' : 1000, 'msg' : '成功'}
#    data = request.json
#
#    logger.info('request data => {0}'.format(data))
#
#    command     = data.get("cmd") or ''
#    user_id     = data.get("data").get("userid") or 0
#    req_user_id = data.get("data").get("req_user_id") or 0
#    page_num    = data.get("data").get("page_num") or 1
#
#    if not command or not user_id or not check_param(data):
#        return handle_param_error()
#
#    service = VideoService()
#    try:
#        result = service.get_video_by_user(user_id, req_user_id, page_num)
#        res    = handle_success(result, 1000, '成功')
#        logger.info('success|user video list request serve success')
#    except:
#        res = handle_failure()
#        logger.error('fail|exception|user video list request serve error|%s' % traceback.format_exc())
#    finally:
#        service.close()
#
#    return res

# 互相关注的接口
@app.route('/user/watch/other', methods=['POST'])
def add_watch():
    logger.info('rec a user watch request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    command     = data.get("cmd") or ''
    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    status      = data.get("status") or 0

    if not command or not user_id or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.watch(user_id, req_user_id, status)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user watch request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|user watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@app.route('/user/fans', methods=['POST'])
def get_fans():
    logger.info('rec a user fans request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json

    command     = data.get("cmd") or ''
    logger.info('request data => {0}'.format(data))
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 0

    if not command or not user_id or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_fans(req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user fans request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|user fans request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@app.route('/user/watchs', methods=['POST'])
def get_watch():
    logger.info('rec a user watch request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 0

    if not command or not user_id or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.get_watch(req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user watch request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|user watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@app.route('/tag/game/all', methods=['POST'])
def get_all_game():
    logger.info('rec a game list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id     = data.get("userid") or 0

    if not command or not check_param(data):
        return handle_param_error()

    service = TagService()
    try:
        result = service.get_all_content()
        res    = handle_success(result, 1000, '成功')
        logger.info('success|game list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|game list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

@app.route('/user/profile/is/watch', methods=['POST'])
def is_watch():
    logger.info('rec a is watch request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0

    if not command or not user_id or not check_param(data):
        return handle_param_error()

    service = ProfileService()
    try:
        result = service.user_watch_relation(user_id, req_user_id)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|is watch request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|is watch request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 个人信息串烧视频接口
@app.route('/video/user/chuan/list', methods=['POST'])
def get_user_chuan_video():
    logger.info('rec a user chuan video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 1

    if not command or not user_id or not check_param(data):
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

# 个人信息观看记录接口
@app.route('/video/user/see/history', methods=['POST'])
def get_user_see_history():
    logger.info('rec a user history video list request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    command     = data.get("cmd") or ''
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id     = data.get("userid") or 0
    req_user_id = data.get("req_user_id") or 0
    page_num    = data.get("page_num") or 1

    if not command or not user_id:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_user_see_history(user_id, req_user_id, page_num)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|user history video list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|user history video list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@app.route('/test/login', methods=['GET'])
def login():
    logger.info('rec a login request')
    res  = {'code' : 1000, 'msg' : '成功'}

    logger.info('request header => {0}'.format(request.headers))
    logger.info('request cookie => {0}'.format(request.cookies))
    logger.info('request code => {0}'.format(request.args.get('code')))

    return jsonify(res)


# 获取观看记录(串烧时)
@app.route('/chuan/video/history/query', methods=['POST'])
def chuan_video_query():
    logger.info('rec a chuan history query request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id = data.get("userid") or 0

    if not user_id:
        return handle_param_error()

    service = HistoryService()
    try:
        result = service.get_chuan_history(user_id=user_id)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|chuan history query list request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|chuan history query list request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

# 获取视频播放url
@app.route('/video/url/query', methods=['POST'])
def get_video_url():
    logger.info('rec a url query request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    logger.info('request data => {0}'.format(data))

    user_id = data.get("userid") or 0
    vid = data.get("vid") or ''

    if not vid:
        return handle_param_error()

    service = VideoService()
    try:
        result = service.get_url_by_vid(vid=vid)
        if not result['url']:
            return handle_param_error()

        res    = handle_success(result, 1000, '成功')
        logger.info('success|url query request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|url query request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res

#查询名字
@app.route('/chuan/title/query', methods=['POST'])
def query_chuan_job_title():
    logger.info('rec a chuan title query request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not check_param(data):
        return handle_param_error()

    uid  = data.get('userid') or 0
    #duration  = data.get('data').get('duration') or 0
    vids = data.get('video_ids') or []
    if not (uid and vids and len(vids)):
        logger.info('fail|userid or vid is null, return')
        return handle_param_error()

    s = ChuanService()
    try:
        result = s.query_title(uid=uid, vids=vids)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|chuan/title/query request serve success:%s'%res)
    except:
        res = handle_failure()
        logger.error('fail|exception|chuan/title/query request serve error|%s' % traceback.format_exc())
    finally:
        s.close()

    return res


@app.route('/history/add', methods=['POST'])
def add_history():
    res = {'code':1000,'msg':'success'}
    data = request.json
    logger.info('add histroy request data => {0}'.format(data))

    data = data.get('data')
    if not check_param(data):
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
        logger.info('success|add history request serve success')
    except:
        res = handle_failure()
        logger.error('fail|exception|add history request serve error|%s' % traceback.format_exc())
    finally:
        service.close()

    return res


@app.route('/')
def hi():
    return 'Hi'



def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
