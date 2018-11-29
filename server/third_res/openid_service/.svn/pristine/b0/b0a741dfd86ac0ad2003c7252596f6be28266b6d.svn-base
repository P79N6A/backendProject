import sys
from lib.httptool import open_url_json
from lib.log import get_logger

logger = get_logger('openid')

class OpenidService(object):
    def __init__(self, ip, port, appname):
        self.ip = ip
        self.port = port
        self.appname = appname

    def openid_to_commid(self, openid_list):
        url = 'http://%s:%s/innerapi/acctapi/transid/openid_to_commid?appname=%s' % (self.ip,self.port,self.appname)
        data = {}
        data['openid_list'] = openid_list

        tmp = open_url_json(url=url, data=data)
        if tmp and isinstance(tmp, dict) and tmp.has_key("commid_list"):
            logger.info('get commid_list success.')
            return tmp["commid_list"]
        else:
            logger.warn('[WARN]get commid_list failed.')
            return ''

    def commid_to_openid(self, commid_list, appid):
        url = 'http://%s:%s/innerapi/acctapi/transid/commid_to_openid?appname=%s' % (self.ip,self.port,self.appname)
        data = {}
        data['appid'] = appid
        data['commid_list'] = commid_list

        tmp = open_url_json(url=url, data=data)
        if tmp and isinstance(tmp, dict) and tmp.has_key("data"):
            logger.info('get openid_list success.')
            return tmp["data"]
        else:
            logger.warn('[WARN]get openid_list failed.')
            return ''

    def openid_to_openid(self, openid_list, target_appid):
        url = 'http://%s:%s/innerapi/acctapi/transid/openid_to_openid?appname=%s' % (self.ip,self.port,self.appname)
        data = {}
        data['target_appid'] = target_appid
        data['openid_list'] = openid_list

        logger.info('post url:%s'%url)
        logger.info('post data:%s'%data)
        tmp = open_url_json(url=url, data=data)
        if tmp and isinstance(tmp, dict) and tmp.has_key("openid_list") and len(tmp["openid_list"]):
            logger.info('get openid_list success.')
            openid_map = {}
            for item in tmp["openid_list"]:
                openid_map[item['source_openid']] = item['target_openid']
            return openid_map
        else:
            logger.warn('[WARN]get openid_list failed.')
            logger.warn(tmp)
            return ''

if __name__ == "__main__":
    from l5.get_router import get_router
    modid,cmdid = (64048833,65537)
    host,port = get_router(modid, cmdid)
    if not (host and port):
        print 'get l5 error'
        sys.exit(1)
    src_app_name = 'newbridge'
    lp_app_name  = 'GPCD_MOBILE_GAME_VIDEO_SDK'
    targ_appid   = 'wx3566ceb82d2e0f2d'
    lp_appid     = 'wx9ce8f64a4c9b3308'
    #openid_list = ['o6zB8wbacab7ATy1PKC3LcG-dgwQ']
    openid_list = ['o1AUX0gpe9fiQB42C8SBA7PbvSfY']

    #open_s = OpenidService(host, port, lp_app_name)
    open_s = OpenidService(host, port, src_app_name)
    #res = open_s.openid_to_openid(openid_list, targ_appid)
    res = open_s.openid_to_openid(openid_list, lp_appid)
    print res
