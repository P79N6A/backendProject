import urllib

from lib.httptool import open_url
from lib.tool import get_session
from lib.log import get_logger
from lib.config import read_link_domain

logger = get_logger('login')

Domain = read_link_domain()

class QQLoginService(object):
    def __init__(self, appid='', secret='', redirect_uri=''):
        self.appid  = appid
        self.secret = secret
        self.redirect_uri = redirect_uri or 'http://nbstorage.sparta.html5.qq.com/qq/code/get'

    def get_user_info_by_code(self, code):
        if not (code and self.appid and self.secret and self.redirect_uri):
            logger.warn('args error, code:%s, appid:%s, secret:%s, redirect_uri:%s'%(code, self.appid, self.secret, self.redirect_uri))
            return None,None,None
        args = (Domain, urllib.quote(code), urllib.quote(self.redirect_uri),urllib.quote(self.appid),urllib.quote(self.secret))
        get_info_url = "http://%s/qq/code/get?code=%s&ruri=%s&qqappid=%s&qqappsecret=%s"%args
        tmp = open_url(get_info_url)
        logger.info('get_user_info_by_code info:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.get('code')==1:
            obj     = tmp.get("data")
            token   = tmp.get("token")
            openid  = tmp.get("openid")
            expires = tmp.get("expires")

            if not (obj and token and expires):
                logger.warn('get user info by code fail, code:%s'%code)
                return None,None,None

            return token, obj, expires

        else:
            logger.warn('get user info by code fail, code:%s'%code)
            return None,None,None


    def get_user_info_by_token(self, openid='',access_token=''):
        if not (access_token and self.appid and self.secret):
            logger.warn('args error, access_token:%s, appid:%s, secret:%s'%(access_token, self.appid, self.secret))
            return None,None,None

        args = (Domain, urllib.quote(openid),urllib.quote(access_token),urllib.quote(self.appid),urllib.quote(self.secret))
        get_info_url = "http://%s/qq/token/valid?openid=%s&token=%s&qqappid=%s&qqappsecret=%s"%args
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

