# -*- coding: UTF-8 -*-
import sys
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/links')
from lib.httptool import open_url
#from service.timeout_service import TimeoutService


from lib.log import get_logger
logger = get_logger('token')

'''
access_token 不存，仅存refresh_token。
将access_token返回给客户端,客户端通过access_token获取相关信息。
'''
class TokenService(object):
    def __init__(self, appid='', secret='', cache=''):
        self.appid  = appid
        self.secret = secret
        if not cache:
            raise Exception('need cahce')
        self.cache  = cache
        #refresh token expire sec
        self.exp_sec = 24 * 60 * 60 * 30
    '''
    如果客户端传来的access_token有效则返回数据;若无效，则：
    首先，将access_token转化为openid。然后需要拿到openid对应的refresh_token。
        若拿不到说明此次请求无效，需重新授权登陆。
        若拿到refresh_token,有效返回数据;若此refresh_token拿不到对应的token和openid，说明以及过期，需要重新授权登陆。
    '''
    def get_user_info_by_code(self, code):
        if code:
	    logger.info('start get_user_info_by_code, code:%s'%code)
            data = self._get_token_by_code(code)
            if data:
                token,refresh_token,openid,expire = data
            if token and refresh_token and openid and expire:
                logger.info('get_token_by_code success,token:%s,ref_token:%s,openid:%s,expire:%s'%data)
                self.cache.add_session(pool='wx_token_openid', k=token, v=openid, expire=self.exp_sec)
                self.cache.add_session(pool='wx_openid_refresh_token', k=openid, v=refresh_token,expire=self.exp_sec)
                obj = self._get_weixin_userinfo(token, openid)
                return (token, obj, openid)
            else:
                logger.error('get token by code failed, token:%s, refresh_token:%s, openid:%s'\
                            (token,refresh_token,openid, expire))
                return ('','','')
        else:
            logger.error('need code')
            return ('','','')

    def get_user_info(self, openid='', access_token=''):
        obj    = None
        token  = ''
        if access_token and openid:
            openid_session = self.cache.get_session(pool='wx_token_openid', k=access_token)
            ##没有记录，需要重新登录
            if not openid or not access_token or not openid==openid_session:
                logger.warn('session valid fail, need login.')
                return None,None,None
            logger.info('get openid:%s by token from cache'%openid)
            obj = self._get_weixin_userinfo(access_token, openid)
            #token过期，重新获取
            if not obj:
                logger.warn('access_token expired, refresh.')
                self.cache.clear_session(pool='wx_token_openid', k=access_token)
                token, openid = self._refresh_token_session(openid)
                if token and openid:
                    logger.info('refresh token success, add to cache. token:%s, openid:%s'%(token, openid))
                    self.cache.add_session(pool='wx_token_openid', k=token, v=openid, expire=self.exp_sec)
                    obj = self._get_weixin_userinfo(token, openid)
            else:
                #没有过期，token不变
                logger.info('token is not expires, use old token:%s, obj:%s'% (access_token, obj))
                token = access_token
        else:
            logger.error('need access_token')

        return (token, obj, openid)

    def _clear_refresh_token(self, openid):
        def func():
            self.cache.clear_session(pool='wx_openid_refresh_token', k=openid)
        return func

    def _refresh_token_session(self, openid):
        refresh_token = self.cache.get_session(pool='wx_openid_refresh_token', k=openid)
        if not refresh_token:
            logger.warn('reget access_toke failed, no refresh_token found, need relogin')
            return ('','')
        else:
            logger.info('reget token success')
            token,openid = self._refresh_token(refresh_token)
            if token and openid:
                return token,openid
            else:
                logger.error('refresh token error, refresh_token:%s,need relogin'%refresh_token)
                return ('','')

    def _get_token_by_code(self, code):
        get_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (self.appid, self.secret, code)
        tmp = open_url(get_token_url)
        if tmp and isinstance(tmp, dict) and tmp.has_key("access_token") and tmp.has_key("openid") and tmp.has_key("refresh_token"):
            token         = tmp["access_token"]
            openid        = tmp["openid"]
            refresh_token = tmp["refresh_token"]
            expire        = tmp["expires_in"]
            logger.info('get token success,appid:%s,secret:%s'%(self.appid,self.secret))
            return (token, refresh_token, openid, expire)
        else:
            logger.warn('[WARN]get token failed,appid:%s,secret:%s,code:%s'%(self.appid,self.secret,code))
            return None

    def _refresh_token(self, refresh_token):
        get_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s" % (self.appid, refresh_token)
        tmp = open_url(get_token_url)
        if tmp and isinstance(tmp, dict) and tmp.has_key("access_token") and tmp.has_key("openid"):
            token = tmp.get("access_token")
            openid = tmp.get("openid")
            logger.info('get token success,token:%s,refresh_token:%s,appid:%s'%(token,refresh_token,self.appid))
            return (token, openid)
        else:
            logger.warn('[WARN]refresh token failed,appid:%s,refresh_token:%s'%(self.appid,refresh_token))
            logger.warn('tmp:%s' % tmp)
            return None

    def _get_weixin_userinfo(self, access_token, openid):
        get_userinfo_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s" % (access_token, openid)
        tmp = open_url(get_userinfo_url)
        if tmp and isinstance(tmp, dict) and tmp.get("nickname") and tmp.get('sex') and tmp.get('headimgurl'):
            obj = {}
            obj['nickname'] = tmp.get("nickname")
            obj['sex']      = tmp.get('sex')
            obj['sex']      = '男' if obj['sex'] == 1 else '女'
            obj['usericon'] = tmp.get('headimgurl')
            obj['openid']   = openid
            logger.info('get userinfo success,info:%s'%obj)
            return obj
        else:
            logger.warn('access_token:%s expired.'%access_token)
            return None


