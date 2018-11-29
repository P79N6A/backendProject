import sys
#sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/links')
#from lib.httptool import open_url
#from lib.httptool import open_url_json
#from lib.taf
from taf.proto.city.SessionObj import Oidb0x70fReq
from taf.proto.city.SessionObj import SessionObjProxy
from lib.log import get_logger

logger = get_logger('openid')

class QQBinaryOpenidService(object):
    def __init__(self, ddwUin=0, dwModuleID=0, wServiceType=0, dwAppID=0):
        self.ddwUin = ddwUin or 271706757
        self.dwModuleID = dwModuleID or 0
        self.wServiceType = wServiceType or 200
        self.dwAppID = dwAppID or 101461961
        self.vector = Oidb0x70fReq.vctcls_adwUins()
        self.proxy_url = "City.SessionServer.SessionObj@tcp -h 10.191.9.94 -p 10127"

    def qq_to_openid(self, uin_list):
        if not (uin_list and isinstance(uin_list, list) and len(uin_list)):
            logger.error('uin_list arg is illegal')
            return
        proxy = SessionObjProxy()
        proxy.locator(self.proxy_url)

        #assemble request
        req = Oidb0x70fReq()
        req.ddwUin = self.ddwUin
        req.dwModuleID = self.dwModuleID
        req.wServiceType = self.wServiceType
        #req.acSessionKey = ''
        req.dwAppID = self.dwAppID
        self.vector.extend(uin_list)
        req.adwUins = self.vector

        #send req
        ret, resp = proxy.oidb0x70f(req)

        #parse response
        uin_openid_map = self._parse_resp(resp)
        return uin_openid_map

    def _parse_resp(self, resp):
        result = {}
        openids = resp.openids
        if openids and len(openids):
            for obj in openids:
                result[obj.dwUin] = obj.openid
        #...

        return result

if __name__ == "__main__":
    uin_list = [289296918,271706757]
    service = QQBinaryOpenidService()
    res = service.qq_to_openid(uin_list)

    print res
