# -*- coding: UTF-8 -*-
import traceback

from flask import Blueprint,request,redirect,jsonify
from lib.log import get_logger
from service.qq_login_service import QQLoginService
from service.weixin_login_service import WeiXinLoginService
from service.user_profile_service import ProfileService
from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

login_service = Blueprint('login_service', __name__)

logger = get_logger('login')

QQ_APP_ID = "101461961"
QQ_APP_SECRET = "fdc67d7cbcfd7ad242a851741fb0447b"

WX_APP_ID = "wx3566ceb82d2e0f2d"
WX_APP_SECRET = "5875415689224b02f05fb40ebb71db8e"

#登陆相关
@login_service.route('/qq/code/get')
def get_qq_code():
    res = {'code':1000,'msg':'success'}
    codee = request.args.get("code")
    if not codee:
        logger.info('fail|code arg not found, return')
        return handle_param_error()

    try:
        logger.info('get qq codee:%s'%codee)

        loginS = QQLoginService(appid=QQ_APP_ID, secret=QQ_APP_SECRET)
        token,obj,expires = loginS.get_user_info_by_code(codee)
        if not (token and obj):
            logger.info('fail|get_user_info_by_code fail,code:%s, return'%codee)
            res['code'] = -1
            res['msg'] = 'login fail'
            return jsonify(res)

        #chuan_id = get_chuan_id_by_openid(openid)
        ps = ProfileService()
        userid = ps.insert_user_profile(obj)

        #nickname = urllib.quote(obj['nickname'])
        #usericon = urllib.quote(obj['usericon'])
        #expires  = urllib.quote(expires)

        logger.info('token:%s, obj:%s, expires:%s, userid:%s'%(token,obj,expires,userid))

        return redirect("http://nbstorage.sparta.html5.qq.com/qq/code/result?token=%s&userid=%s"%(token,userid), code=302)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())

    return res

@login_service.route('/qq/login/access_token')
def valid_access_token():
    res = {'code':1000,'msg':'success','data':{}}
    token = request.args.get("token")
    userid = request.args.get("userid")
    if not (token and userid):
        logger.info('fail|code or userid arg not found, return')
        res['code'] = -1
        res['msg'] = 'need code and userid'
        return handle_param_error()

    logger.info('get qq token:%s, userid:%s'%(token,userid))
    ps = ProfileService()

    openid = ps.get_uid_by_userid(userid)
    try:
        token_serv = QQLoginService(appid=QQ_APP_ID, secret=QQ_APP_SECRET)
        token,session,obj = token_serv.get_user_info_by_token(openid=openid, access_token=token)
        if not (token and session and obj):
            logger.info('fail|get_user_info_by_code fail,token:%s,session:%s, obj:%s.'%(token,session,obj))
            res['code'] = -1
            res['msg'] = 'login fail'
            return handle_failure()

        result = {}
        result['token']   = token
        result['session'] = session
        #data['userinfo'] = obj

        ps.update_user_profile(obj)

        res    = handle_success(result, 1000, '成功')
        logger.info('valid_access_token response:%s'%result)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())

    finally:
        ps.close()

    return res

@login_service.route('/qq/code/result')
def get_qq_code_result():
    res = {'code':1000,'msg':'success'}
    #codee = request.args.get("code")
    token = request.args.get("token")
    userid = request.args.get("userid")
    if not (token and userid):
        logger.info('fail|token userid arg not found, return')
        res['code'] = -1
        res['msg'] = 'need token and userid.'
        return handle_param_error()

    logger.info('result get token:%s, userid:%s'%(token,userid))

    return jsonify(res)


@login_service.route('/weixin/code/get')
def get_weixin_code():
    res = {'code':1000,'msg':'success'}
    codee = request.args.get("code")
    if not codee:
        logger.info('fail|code arg not found, return')
        return handle_param_error()

    try:
        logger.info('get weixin codee:%s'%codee)

        loginS = WeiXinLoginService(appid=WX_APP_ID, secret=WX_APP_SECRET)
        token,obj = loginS.get_user_info_by_code(codee)
        obj['uid_type'] = 2
        if not (token and obj):
            logger.info('fail|get_user_info_by_code fail,code:%s, return'%codee)
            return handle_failure()


        #chuan_id = get_chuan_id_by_openid(openid)
        ps = ProfileService()
        userid = ps.insert_user_profile(obj)
        if not userid:
            obj    = ps.get_user_profile_by_uid(obj['openid'])
            if obj:
                userid =  obj['userid']

        if not userid:
            logger.warn('fail|get_user_info_by_code fail,userid is null,code:%s, return'%codee)
            return handle_failure()

        #nickname = urllib.quote(obj['nickname'])
        #usericon = urllib.quote(obj['usericon'])
        #expires  = urllib.quote(expires)
        result = {}
        result['token']   = token
        result['userid']  = userid
        res = handle_success(result, 1000, '成功')
        logger.info('get_weixin_code response:%s'%result)

        #return redirect("http://nbstorage.sparta.html5.qq.com/qq/code/result?token=%s&userid=%s"%(token,userid), code=302)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())

    return res

@login_service.route('/weixin/login/access_token')
def valid_wx_access_token():
    res = {'code':1000,'msg':'success','data':{}}
    token = request.args.get("token")
    userid = request.args.get("userid")
    if not (token and userid):
        return handle_param_error()

    logger.info('get weixin token:%s, userid:%s'%(token,userid))
    ps = ProfileService()

    openid = ps.get_uid_by_userid(userid)
    try:
        token_serv = WeiXinLoginService(appid=WX_APP_ID, secret=WX_APP_SECRET)
        token,session,obj = token_serv.get_user_info_by_token(openid=openid, access_token=token)
        if not (token and session and obj):
            logger.info('fail|valid_wx_access_token fail,token:%s,session:%s, obj:%s.'%(token,session,obj))
            return handle_failure()

        result = {}
        result['token']   = token
        result['session'] = session
        #data['userinfo'] = obj

        ps.update_user_profile(obj)

        res = handle_success(result, 1000, '成功')
        logger.info('valid_wx_access_token response:%s'%result)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())

    finally:
        ps.close()

    return res

@login_service.route('/weixin/signature/get')
def get_weixin_signature():
    res = {'code':1000,'msg':'success','data':{}}
    logger.info('get a weixin signature req')

    try:
        token_serv = WeiXinLoginService(appid=WX_APP_ID, secret=WX_APP_SECRET)
        data = token_serv.get_signature()
        if not data:
            logger.info('fail|get_signature fail.')
            #res['code'] = -1
            #res['msg'] = 'signature fail'
            return handle_failure()

        result = {}
        result['signature'] = data[0]
        result['ts']        = data[1]
        result['noncestr']  = data[2]
        #data['userinfo'] = obj

        res = handle_success(result, 1000, '成功')
        logger.info('get weixin signature response:%s'%result)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())

    finally:
        pass

    return res
