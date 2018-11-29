# -*- coding: UTF-8 -*-
import sys
import time
import urllib
import traceback

from flask import Flask,jsonify,request,redirect
from service.signature import SignatureService
from service.token_service import TokenService 
from service.qq_token_service import QQTokenService 
from commonlib.service.session_service import SessionService
from lib.log import get_logger

logger = get_logger('main')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

WX_APP_NAME   = "newbridge"
WX_APP_ID     = "wx3566ceb82d2e0f2d"
WX_APP_SECRET = "5875415689224b02f05fb40ebb71db8e"

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/weixin/signature/get')
def get_signature():
    ts = str(long(time.time()))
    noncestr = "noncestr"
    res = {'code':1,'msg':'success', 'signature':'', 'ts':ts, 'noncestr':noncestr}

    cache = SessionService()
    try:
        sig_serv = SignatureService(WX_APP_ID, WX_APP_SECRET, cache)
        sig = sig_serv.get_signature(ts, noncestr)
        if sig:
            res['signature'] = sig
        else:
            res['code'] = -1
    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        cache.close()

    return jsonify(res)

@app.route('/weixin/code/get')
def get_info_by_code():

    cache = SessionService()
    try:
        res = {'code':1,'msg':'success', 'session':'', 'userinfo':''}
        code = request.args.get("code")
        APP_ID = request.args.get("qqappid")
        APP_SECRET = request.args.get("qqappsecret")

        if not (code and APP_ID and APP_SECRET):
            logger.info('fail|args error, return')
            res['code'] = -1
            res['msg'] = 'need code, appid, secret'
            return jsonify(res)

        code = urllib.unquote(code)
        APP_ID = urllib.unquote(APP_ID)
        APP_SECRET = urllib.unquote(APP_SECRET)

        token_serv = TokenService(appid=APP_ID, secret=APP_SECRET, cache=cache)
        token,obj,openid = token_serv.get_user_info_by_code(code)
        if token and obj:
            res['token'] = token
            res['data'] = obj
            res['openid'] = openid

        return jsonify(res)

    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        cache.close()


@app.route('/weixin/token/valid')
def get_info_by_access():
    res = {'code':1,'msg':'success','data':{}}
    openid = request.args.get("openid")
    token  = request.args.get("token")
    APP_ID = request.args.get("qqappid")
    APP_SECRET = request.args.get("qqappsecret")
    if not (openid and token and APP_ID and APP_SECRET):
        logger.info('fail|token APP_ID APP_SECRET arg not found, return')
        res['code'] = -1
        res['msg'] = 'arg invalid'
        return jsonify(res)

    cache = SessionService()
    try:
        logger.info('get qq token arg:%s, openid:%s'%(token, openid))

        openid     = urllib.unquote(openid)
        token      = urllib.unquote(token)
        APP_ID     = urllib.unquote(APP_ID)
        APP_SECRET = urllib.unquote(APP_SECRET)

        token_serv = TokenService(appid=APP_ID, secret=APP_SECRET, cache=cache)
        token,obj,openid = token_serv.get_user_info(openid=openid, access_token=token)
        if not (token and obj and openid):
            logger.info('fail|valid_token fail,token:%s, return'%token)
            res['code'] = -1
            res['msg'] = 'valid fail'
            return jsonify(res)

        res['data']   = obj
        res['token']  = token
        res['openid'] = openid
        logger.info('valid_token response:%s'%res)

        return jsonify(res)

    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        cache.close()

@app.route('/qq/code/get')
def get_qq_code():
    res = {'code':1,'msg':'success','data':{}}
    codee = request.args.get("code")
    redirect_uri = request.args.get("ruri")
    QQ_APP_ID = request.args.get("qqappid")
    QQ_APP_SECRET = request.args.get("qqappsecret")

    if not (codee and redirect_uri and QQ_APP_ID and QQ_APP_SECRET):
        logger.info('fail|code or redirect_uri QQTokenService QQ_APP_SECRET arg not found, return')
        res['code'] = -1
        res['msg'] = 'args invalid'
        return jsonify(res)

    cache = SessionService()
    try:
        codee         = urllib.unquote(codee)
        redirect_uri  = urllib.unquote(redirect_uri)
        QQ_APP_ID     = urllib.unquote(QQ_APP_ID)
        QQ_APP_SECRET = urllib.unquote(QQ_APP_SECRET)
        logger.info('get qq arg codee:%s, redirect_uri:%s'%(codee,redirect_uri))

        token_serv = QQTokenService(appid=QQ_APP_ID, secret=QQ_APP_SECRET, redirect_uri=redirect_uri, cache=cache)
        token,obj,openid,expires = token_serv.get_user_info_by_code(codee)
        if not (token and obj):
            logger.info('fail|get_user_info_by_code fail,code:%s, return'%codee)
            res['code'] = -1
            res['msg'] = 'login fail'
            return jsonify(res)

        obj['openid'] = openid

        res['data']    = obj
        res['token']   = token
        res['openid']  = openid
        res['expires'] = expires

        logger.info('get_qq_code response:%s'%res)

        return jsonify(res)
    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        cache.close()


@app.route('/qq/token/valid')
def valid_token():
    res = {'code':1,'msg':'success','data':{}}
    token  = request.args.get("token")
    openid = request.args.get("openid")
    QQ_APP_ID = request.args.get("qqappid")
    QQ_APP_SECRET = request.args.get("qqappsecret")
    if not (openid and token and QQ_APP_ID and QQ_APP_SECRET):
        logger.info('fail|token QQ_APP_ID QQ_APP_SECRET arg not found, return')
        res['code'] = -1
        res['msg'] = 'arg invalid'
        return jsonify(res)

    cache = SessionService()
    try:
        logger.info('get qq token arg:%s, openid:%s'%(token,openid))

        token  = urllib.unquote(token)
        openid = urllib.unquote(openid)
        QQ_APP_ID     = urllib.unquote(QQ_APP_ID)
        QQ_APP_SECRET = urllib.unquote(QQ_APP_SECRET)


        token_serv = QQTokenService(appid=QQ_APP_ID, secret=QQ_APP_SECRET, cache=cache)
        token,obj,openid = token_serv.get_user_info(openid=openid, access_token=token)
        if not (token and obj and openid):
            logger.info('fail|valid_token fail,token:%s, return'%token)
            res['code'] = -1
            res['msg'] = 'valid fail'
            return jsonify(res)

        res['data']   = obj
        res['token']  = token
        res['openid'] = openid
        logger.info('valid_token response:%s'%res)

        return jsonify(res)

    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        cache.close()


@app.route('/weixin/openid/convert', methods=['POST'])
def convert_wx_openid():
    res = {'code':1,'msg':'success','data':{}}
    data = request.json
    openid_list  = data.get("openid_list")
    target_appid = data.get('target_appid')
    if not (openid_list and len(openid_list) and target_appid):
        logger.info('fail|openid_list target_appid arg not found, return')
        res['code'] = -1
        res['msg'] = 'arg invalid'
        return jsonify(res)

    try:
        from l5.get_router import get_router
        from service.openid_service import OpenidService
        modid,cmdid = (64048833,65537)
        host,port = get_router(modid, cmdid)
        if not (host and port):
            logger.error('get wx openid service host and port error.')
            res['code'] = -2
            res['msg'] = 'internal error'
            return jsonify(res)
        logger.info('get wx openid convert req. openid_list:%s, target_appid:%s'%(openid_list, target_appid))
        
        open_s = OpenidService(host, port, WX_APP_NAME)
        data = open_s.openid_to_openid(openid_list, target_appid)
        if not res:
            logger.warn('convert fail.')
            res['code'] = -3
            res['msg']  = 'convert fail'
            return jsonify(res)

        res['data'] = data
        logger.info('convert_wx_openid response:%s'%res)

        return jsonify(res)

    except:
        res['code'] = -1
        res['msg'] = 'internal error'
        logger.error(traceback.format_exc())
        return jsonify(res)
    finally:
        pass



@app.route('/')
def hi():
    return 'Hi'
