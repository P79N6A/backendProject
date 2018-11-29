import sys
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/links')

import time
import hashlib
from lib.httptool import open_url
from lib.log import get_logger

logger = get_logger('signature')

class SignatureService(object):
    def __init__(self, appid, secret, cache):
        self.appid  = appid
        self.secret = secret
        self.cache  = cache

    def _clear_ticket_session(self, appid):
        def func():
            self.cache.clear_session(pool='sig', k=appid)
        return func

    def get_signature(self, ts, noncestr):
        #ticket = SessionService().get_session(pool='sig',k=self.appid)
        ticket = ''
        if ticket:
            logger.info('get ticket from session cache:%s' % ticket)
        else:
            logger.info('session cache has no ticket, start fetch from service.')
            ticket = self._get_sdk_ticket()
            #TimeoutService().add_timeout(self.appid, 7000,
            #                             self._clear_ticket_session(self.appid))
            #if ticket:
            #    SessionService().add_session(pool='sig',k=self.appid,v=ticket)


        if ticket:
            logger.info('ts:%s, noncestr:%s, ticket:%s'%(ts,noncestr,ticket))
            sig = self.signature(appid=self.appid, sdk_ticket=ticket,
                            noncestr=noncestr, timestamp=ts)
            if sig:
                logger.info('get signature success,signature:%s'%sig)
            return sig

    def _get_token(self):
        get_atk_url = "https://api.weixin.qq.com/cgi-bin/token?appid=%s&secret=%s&grant_type=client_credential" % (self.appid, self.secret)
        tmp = open_url( get_atk_url )
        if tmp and isinstance(tmp, dict) and tmp.has_key("access_token"):
            logger.info('get access_token success,appid:%s,secret:%s'%(self.appid,self.secret))
            return tmp["access_token"]
        else:
            logger.warn('[WARN]no access_token, appid:%s,secret:%s'%(self.appid,self.secret))
            return ''

    def _get_sdk_ticket(self):
        access_token = self._get_token()
        if access_token:
            get_ticket_url="http://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=2" % access_token
            tmp = open_url(get_ticket_url)
            if tmp and isinstance(tmp, dict) and tmp.has_key('ticket'):
                return tmp['ticket']
            else:
                logger.warn('[WARN]no ticket, access_token:%s'%access_token)
        else:
            logger.warn('[WARN]get access_token fail')

        return ''

    def signature(self, **dic):
        x = [k+"="+dic[k] for k in dic]
        x.sort()
        return hashlib.sha1(("&".join(x)).encode()).hexdigest()

if __name__ == "__main__":
    s = SignatureService('wx3566ceb82d2e0f2d','5875415689224b02f05fb40ebb71db8e')
    sig1 = s.get_signature()
    sig2 = s.get_signature()
    #time.sleep(12)
    sig3 = s.get_signature()
    sig4 = s.get_signature()
    if sig1 and sig2 and sig3:
        print 'success get signature,1:%s,2:%s,3:%s,4:%s'%(sig1,sig2,sig3,sig4)
