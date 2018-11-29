# -*- coding: UTF-8 -*-
import sys
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/links')
from lib.httptool import open_url,open_url_kv,open_url_jsonp


from lib.log import get_logger
logger = get_logger('token')

'''
access_token 不存，仅存refresh_token。
将access_token返回给客户端,客户端通过access_token获取相关信息。
'''
class QQTokenService(object):
    def __init__(self, appid='', secret='', redirect_uri='', cache=None):
        self.appid  = appid
        self.secret = secret
        self.redirect_uri = redirect_uri or 'http://nblinks.sparta.html5.qq.com/qq/code/get'
        self.cache  = cache
        if not cache:
            raise Exception("need cache.")
        self.exp_sec = 24 * 60 * 60 * 30
    '''
    如果客户端传来的access_token有效则返回数据;若无效，则：
    首先，将access_token转化为openid。然后需要拿到openid对应的refresh_token。
        若拿不到说明此次请求无效，需重新授权登陆。
        若拿到refresh_token,有效返回数据;若此refresh_token拿不到对应的token和openid，说明以及过期，需要重新授权登陆。
    '''
    def get_user_info_by_code(self, code):
        token,refresh_token,openid,expires = ('', '','',0)
        if code:
	    logger.info('start get_user_info_by_code, code:%s'%code)
            result = self._get_token_by_code(code)
            if result:
                token,refresh_token,openid,expires = result
            if token and refresh_token and openid:
		logger.info('get_token_by_code success,token:%s,ref_token:%s,openid:%s,exp:%s'%(token,refresh_token,openid,expires))
                self.cache.add_session(pool='qq_token_openid', k=token, v=openid, expire=self.exp_sec)
                self.cache.add_session(pool='qq_refresh_token', k=openid, v=refresh_token, expire=self.exp_sec)
                obj = self._get_qq_userinfo(token, openid)
                return (token, obj, openid, expires)
            else:
                logger.error('get token by code failed, token:%s, refresh_token:%s, openid:%s'%(token,refresh_token,openid))
                return ('','','',0)
        else:
            logger.error('need code')
            return ('', '','',0)

    def get_user_info(self, access_token='', openid=''):
        obj    = None
        token  = ''
        if access_token and openid:
            openid_session = self.cache.get_session(pool='qq_token_openid', k=access_token)
            if not openid or not access_token or not openid==openid_session:
                logger.warn('session valid fail, need login.')
                return None,None,None

            obj = self._get_qq_userinfo(access_token, openid)
            #token过期，重新获取
            if not obj:
                self.cache.clear_session(pool='qq_token_openid', k=access_token)
                logger.warn('access_token expired, refresh.')
                token, refresh_token = self._refresh_token_session(openid)
                if token and refresh_token:
                    self.cache.add_session(pool='qq_token_openid', k=token, v=openid, expire=self.exp_sec)
                    obj = self._get_qq_userinfo(token, openid)
                    #self.cache.add_session(pool='qq_refresh_token', k=openid, v=refresh_token,expire=self.exp_sec)
            else:
                #没有过期，token不变
                logger.info('token is not expires, use old token:%s, obj:%s'% (access_token, obj))
                token = access_token
        else:
            logger.error('need access_token')

        return (token, obj, openid)

    def _clear_refresh_token(self, openid):
        def func():
            self.cache.clear_session(pool='qq_refresh_token', k=openid)
        return func

    def _refresh_token_session(self, openid):
        refresh_token = self.cache.get_session(pool='qq_refresh_token', k=openid)
        if not refresh_token:
            logger.warn('reget access_toke failed, no refresh_token found, need relogin')
            return ('','')
        else:
            logger.info('reget token success')
            token,refresh_token = self._refresh_token(refresh_token)
            if token and refresh_token:
                return token, refresh_token
            else:
                logger.error('refresh token error, refresh_token:%s,need relogin'%refresh_token)
                return ('','')

    def _get_token_by_code(self, code):
        get_token_url = "https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id=%s&client_secret=%s&code=%s&redirect_uri=%s" % (self.appid, self.secret, code, self.redirect_uri)
	logger.info('get_token_by_code, url:%s'%get_token_url)
        tmp = open_url_kv(get_token_url)
	logger.info('get_token_by_code, res:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.has_key("access_token") and tmp.has_key("expires_in") and tmp.has_key("refresh_token"):
            token = tmp["access_token"]
            expires = tmp["expires_in"]
            refresh_token = tmp["refresh_token"]
            logger.info('get token success,appid:%s,secret:%s'%(self.appid,self.secret))
            get_openid_url = "https://graph.qq.com/oauth2.0/me?access_token=%s"%token
            logger.info('start get openid, url:%s'%get_openid_url)
            tmp = open_url_jsonp(get_openid_url)
            logger.info('get openid res:%s'%tmp)
            if tmp and isinstance(tmp, dict) and tmp.has_key("openid"):
                openid = tmp["openid"]
            else:
                logger.warn('[WARN]get openid failed,access_token:%s'%token)
                return None

            #logger.info('get token by code success,code:%s, access_token:%s, refresh_token:%s, openid:%s'%(code,token,refresh_token,openid))
            return (token, refresh_token, openid, expires)
        else:
            logger.warn('[WARN]get token failed,appid:%s,secret:%s,code:%s'%(self.appid,self.secret,code))
            return None


    def _refresh_token(self, refresh_token):
        get_token_url = "https://graph.qq.com/oauth2.0/token?client_id=%s&grant_type=refresh_token&client_secret=%s&refresh_token=%s" % (self.appid, self.secret,refresh_token)
        logger.info('refresh_token :%s' % get_token_url)
        tmp = open_url_kv(get_token_url)
        if tmp and isinstance(tmp, dict) and tmp.has_key("access_token"):
            token = tmp.get("access_token")
            refresh_token = tmp.get("refresh_token")
            logger.info('get token success,token:%s,refresh_token:%s,appid:%s'%(token,refresh_token,self.appid))
            return (token, refresh_token)
        else:
            logger.warn('[WARN]refresh token failed,appid:%s,refresh_token:%s'%(self.appid,refresh_token))
            logger.warn('tmp:%s' % tmp)
            return None

    def _get_qq_userinfo(self, access_token, openid):
        get_userinfo_url = "https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s" % (access_token, self.appid, openid)
        logger.info('start get_qq_userinfo, url:%s'%get_userinfo_url)
        tmp = open_url(get_userinfo_url)
        logger.info('get_qq_info:%s'%tmp)
        if tmp and isinstance(tmp, dict) and tmp.get("nickname") and tmp.get('gender') and tmp.get('figureurl_qq_1'):
            obj = {}
            obj['nickname'] = tmp.get("nickname")
            obj['sex']      = tmp.get('gender')
            obj['usericon'] = tmp.get('figureurl_qq_2') or tmp.get('figureurl_qq_1')
            obj['openid']   = openid
            logger.info('get userinfo success,nickname:%s,sex:%s,headimgurl:%s,openid:%s'%(obj['nickname'],obj['sex'],obj['usericon'],openid))
            return obj
        else:
            logger.warn('access_token:%s expired.'%access_token)
            return None

