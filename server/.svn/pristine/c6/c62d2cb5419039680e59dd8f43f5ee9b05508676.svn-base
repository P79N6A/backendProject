import urllib

from lib.httptool import open_url
from lib.tool import get_session
from lib.log import get_logger
from lib.config import read_link_domain

logger = get_logger('login')

Domain = read_link_domain()

class WeiXinLoginService(object):
    def __init__(self, appid='', secret=''):
        self.appid  = appid
        self.secret = secret
        #self.redirect_uri = redirect_uri or 'http://nbstorage.sparta.html5.qq.com/qq/code/get'

    def get_signature(self):
        get_signature_url = "http://%s/weixin/signature/get"%Domain
        tmp = open_url(get_signature_url)
        logger.info('get_signature info:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.get('code')==1:
            signature = tmp.get("signature")
            ts        = tmp.get("ts")
            noncestr  = tmp.get("noncestr")

            return (signature, ts, noncestr)

        else:
            logger.warn('get signature fail')
            return None


    def get_user_info_by_code(self, code):
        if not (code and self.appid and self.secret):
            logger.warn('args error, code:%s, appid:%s, secret:%s'%(code, self.appid, self.secret))
            return None,None
        args = (Domain, urllib.quote(code),urllib.quote(self.appid),urllib.quote(self.secret))
        get_info_url = "http://%s/weixin/code/get?code=%s&qqappid=%s&qqappsecret=%s"%args
        tmp = open_url(get_info_url)
        logger.info('get_user_info_by_code info:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.get('code')==1:
            obj     = tmp.get("data")
            token   = tmp.get("token")
            openid  = tmp.get("openid")
            #expires = tmp.get("expires")

            if not (obj and token):
                logger.warn('get user info by code fail, code:%s'%code)
                return None,None

            return token, obj

        else:
            logger.warn('get user info by code fail, code:%s'%code)
            return None,None


    def get_user_info_by_token(self, openid='', access_token=''):
        if not (openid and access_token and self.appid and self.secret):
            logger.warn('args error, openid:%s,access_token:%s, appid:%s, secret:%s'%(openid, access_token, self.appid, self.secret))
            return None,None,None

        args = (Domain, urllib.quote(openid),urllib.quote(access_token),urllib.quote(self.appid),urllib.quote(self.secret))
        get_info_url = "http://%s/weixin/token/valid?openid=%s&token=%s&qqappid=%s&qqappsecret=%s"%args
        tmp = open_url(get_info_url)
        logger.info('get_user_info_by_token info:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.get('code')==1:
            obj     = tmp.get("data")
            openid  = tmp.get("openid")
            token   = tmp.get("token")

            if not (obj and token and openid):
                logger.warn('get_user_info_by_token fail, access_token:%s'%access_token)
                return None,None,None

            session = get_session(openid=openid, token=token)

            return token,session,obj

        else:
            logger.warn('get_user_info_by_token fail, access_token:%s'%access_token)
            return None,None,None

