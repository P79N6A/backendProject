from taf.core import tafcore;
from taf.__rpc import ServantProxy;


class SessionBusiHead(tafcore.struct):
    __taf_class__ = "City.SessionBusiHead";
    
    def __init__(self):
        self.version = 0;
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.version);
    
    @staticmethod
    def readFrom(ios):
        value = SessionBusiHead();
        value.version= ios.read(tafcore.int32, 0, False, value.version);
        return value;

class PtloginSZKeyVerifyReq(tafcore.struct):
    __taf_class__ = "City.PtloginSZKeyVerifyReq";
    
    def __init__(self):
        self.uin = 0;
        self.szKey = "";
        self.clientIp = "";
        self.appId = 0;
        self.qua = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.uin);
        oos.write(tafcore.string, 1, value.szKey);
        oos.write(tafcore.string, 2, value.clientIp);
        oos.write(tafcore.int64, 3, value.appId);
        oos.write(tafcore.string, 4, value.qua);
    
    @staticmethod
    def readFrom(ios):
        value = PtloginSZKeyVerifyReq();
        value.uin= ios.read(tafcore.int64, 0, False, value.uin);
        value.szKey= ios.read(tafcore.string, 1, False, value.szKey);
        value.clientIp= ios.read(tafcore.string, 2, False, value.clientIp);
        value.appId= ios.read(tafcore.int64, 3, False, value.appId);
        value.qua= ios.read(tafcore.string, 4, False, value.qua);
        return value;

class VerifyResult(tafcore.struct):
    __taf_class__ = "City.VerifyResult";
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
    
    @staticmethod
    def readFrom(ios):
        value = VerifyResult();
        value.ret= ios.read(tafcore.int32, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        return value;

class PtloginSZKeyVerifyRsp(tafcore.struct):
    __taf_class__ = "City.PtloginSZKeyVerifyRsp";
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
        self.result = VerifyResult();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
        oos.write(VerifyResult, 2, value.result);
    
    @staticmethod
    def readFrom(ios):
        value = PtloginSZKeyVerifyRsp();
        value.ret= ios.read(tafcore.int32, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        value.result= ios.read(VerifyResult, 2, False, value.result);
        return value;

class WxLoginVerifyReq(tafcore.struct):
    __taf_class__ = "City.WxLoginVerifyReq";
    
    def __init__(self):
        self.openId = "";
        self.token = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.string, 0, value.openId);
        oos.write(tafcore.string, 1, value.token);
    
    @staticmethod
    def readFrom(ios):
        value = WxLoginVerifyReq();
        value.openId= ios.read(tafcore.string, 0, True, value.openId);
        value.token= ios.read(tafcore.string, 1, True, value.token);
        return value;

class WxLoginVerifyRsp(tafcore.struct):
    __taf_class__ = "City.WxLoginVerifyRsp";
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
        self.result = VerifyResult();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
        oos.write(VerifyResult, 2, value.result);
    
    @staticmethod
    def readFrom(ios):
        value = WxLoginVerifyRsp();
        value.ret= ios.read(tafcore.int32, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        value.result= ios.read(VerifyResult, 2, False, value.result);
        return value;

class Oidb0x5e1Req(tafcore.struct):
    __taf_class__ = "City.Oidb0x5e1Req";
    vctcls_uins = tafcore.vctclass(tafcore.int64);
    
    def __init__(self):
        self.uins = Oidb0x5e1Req.vctcls_uins();
        self.szKey = "";
        self.clientIp = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(value.vctcls_uins, 0, value.uins);
        oos.write(tafcore.string, 1, value.szKey);
        oos.write(tafcore.string, 2, value.clientIp);
    
    @staticmethod
    def readFrom(ios):
        value = Oidb0x5e1Req();
        value.uins= ios.read(value.vctcls_uins, 0, False, value.uins);
        value.szKey= ios.read(tafcore.string, 1, False, value.szKey);
        value.clientIp= ios.read(tafcore.string, 2, False, value.clientIp);
        return value;

class QQUserInfo(tafcore.struct):
    __taf_class__ = "City.QQUserInfo";
    
    def __init__(self):
        self.uin = 0;
        self.nick = "";
        self.gender = 0;
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.uin);
        oos.write(tafcore.string, 1, value.nick);
        oos.write(tafcore.int32, 2, value.gender);
    
    @staticmethod
    def readFrom(ios):
        value = QQUserInfo();
        value.uin= ios.read(tafcore.int64, 0, False, value.uin);
        value.nick= ios.read(tafcore.string, 1, False, value.nick);
        value.gender= ios.read(tafcore.int32, 2, False, value.gender);
        return value;

class Oidb0x5e1Rsp(tafcore.struct):
    __taf_class__ = "City.Oidb0x5e1Rsp";
    vctcls_userInfos = tafcore.vctclass(QQUserInfo);
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
        self.userInfos = Oidb0x5e1Rsp.vctcls_userInfos();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
        oos.write(value.vctcls_userInfos, 2, value.userInfos);
    
    @staticmethod
    def readFrom(ios):
        value = Oidb0x5e1Rsp();
        value.ret= ios.read(tafcore.int32, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        value.userInfos= ios.read(value.vctcls_userInfos, 2, False, value.userInfos);
        return value;

class Oidb0x70fReq(tafcore.struct):
    __taf_class__ = "City.Oidb0x70fReq";
    vctcls_adwUins = tafcore.vctclass(tafcore.int64);
    
    def __init__(self):
        self.ddwUin = 0;
        self.dwModuleID = 0;
        self.wServiceType = 0;
        self.acSessionKey = "";
        self.dwAppID = 0;
        self.adwUins = Oidb0x70fReq.vctcls_adwUins();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.ddwUin);
        oos.write(tafcore.int32, 1, value.dwModuleID);
        oos.write(tafcore.int32, 2, value.wServiceType);
        oos.write(tafcore.string, 3, value.acSessionKey);
        oos.write(tafcore.int32, 4, value.dwAppID);
        oos.write(value.vctcls_adwUins, 5, value.adwUins);
    
    @staticmethod
    def readFrom(ios):
        value = Oidb0x70fReq();
        value.ddwUin= ios.read(tafcore.int64, 0, False, value.ddwUin);
        value.dwModuleID= ios.read(tafcore.int32, 1, False, value.dwModuleID);
        value.wServiceType= ios.read(tafcore.int32, 2, False, value.wServiceType);
        value.acSessionKey= ios.read(tafcore.string, 3, False, value.acSessionKey);
        value.dwAppID= ios.read(tafcore.int32, 4, False, value.dwAppID);
        value.adwUins= ios.read(value.vctcls_adwUins, 5, False, value.adwUins);
        return value;

class QQOpenid(tafcore.struct):
    __taf_class__ = "City.QQOpenid";
    
    def __init__(self):
        self.dwUin = 0;
        self.wOpenID_len = 0;
        self.openid = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.dwUin);
        oos.write(tafcore.int32, 1, value.wOpenID_len);
        oos.write(tafcore.string, 2, value.openid);
    
    @staticmethod
    def readFrom(ios):
        value = QQOpenid();
        value.dwUin= ios.read(tafcore.int64, 0, False, value.dwUin);
        value.wOpenID_len= ios.read(tafcore.int32, 1, False, value.wOpenID_len);
        value.openid= ios.read(tafcore.string, 2, False, value.openid);
        return value;

class Oidb0x70fRsp(tafcore.struct):
    __taf_class__ = "City.Oidb0x70fRsp";
    vctcls_openids = tafcore.vctclass(QQOpenid);
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
        self.dwAppID = 0;
        self.wUinOpenID_num = 0;
        self.openids = Oidb0x70fRsp.vctcls_openids();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
        oos.write(tafcore.int32, 2, value.dwAppID);
        oos.write(tafcore.int32, 3, value.wUinOpenID_num);
        oos.write(value.vctcls_openids, 4, value.openids);
    
    @staticmethod
    def readFrom(ios):
        value = Oidb0x70fRsp();
        value.ret= ios.read(tafcore.int32, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        value.dwAppID= ios.read(tafcore.int32, 2, False, value.dwAppID);
        value.wUinOpenID_num= ios.read(tafcore.int32, 3, False, value.wUinOpenID_num);
        value.openids= ios.read(value.vctcls_openids, 4, False, value.openids);
        return value;

class GetXcxSessionKeyByCodeReq(tafcore.struct):
    __taf_class__ = "City.GetXcxSessionKeyByCodeReq";
    
    def __init__(self):
        self.appId = "";
        self.code = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.string, 0, value.appId);
        oos.write(tafcore.string, 1, value.code);
    
    @staticmethod
    def readFrom(ios):
        value = GetXcxSessionKeyByCodeReq();
        value.appId= ios.read(tafcore.string, 0, False, value.appId);
        value.code= ios.read(tafcore.string, 1, False, value.code);
        return value;

class WXErrRsp(tafcore.struct):
    __taf_class__ = "City.WXErrRsp";
    
    def __init__(self):
        self.errcode = 0;
        self.errmsg = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.errcode);
        oos.write(tafcore.string, 1, value.errmsg);
    
    @staticmethod
    def readFrom(ios):
        value = WXErrRsp();
        value.errcode= ios.read(tafcore.int64, 0, False, value.errcode);
        value.errmsg= ios.read(tafcore.string, 1, False, value.errmsg);
        return value;

class XCXSessionRsp(tafcore.struct):
    __taf_class__ = "City.XCXSessionRsp";
    
    def __init__(self):
        self.openid = "";
        self.session_key = "";
        self.expires_in = 0;
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.string, 0, value.openid);
        oos.write(tafcore.string, 1, value.session_key);
        oos.write(tafcore.int64, 2, value.expires_in);
    
    @staticmethod
    def readFrom(ios):
        value = XCXSessionRsp();
        value.openid= ios.read(tafcore.string, 0, False, value.openid);
        value.session_key= ios.read(tafcore.string, 1, False, value.session_key);
        value.expires_in= ios.read(tafcore.int64, 2, False, value.expires_in);
        return value;

class GetXcxSessionKeyByCodeRsp(tafcore.struct):
    __taf_class__ = "City.GetXcxSessionKeyByCodeRsp";
    
    def __init__(self):
        self.ret = 0;
        self.msg = "";
        self.session = XCXSessionRsp();
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int64, 0, value.ret);
        oos.write(tafcore.string, 1, value.msg);
        oos.write(XCXSessionRsp, 2, value.session);
    
    @staticmethod
    def readFrom(ios):
        value = GetXcxSessionKeyByCodeRsp();
        value.ret= ios.read(tafcore.int64, 0, False, value.ret);
        value.msg= ios.read(tafcore.string, 1, False, value.msg);
        value.session= ios.read(XCXSessionRsp, 2, False, value.session);
        return value;

class WXResponse(tafcore.struct):
    __taf_class__ = "City.WXResponse";
    
    def __init__(self):
        self.errcode = 0;
        self.errmsg = "";
    
    @staticmethod
    def writeTo(oos, value):
        oos.write(tafcore.int32, 0, value.errcode);
        oos.write(tafcore.string, 1, value.errmsg);
    
    @staticmethod
    def readFrom(ios):
        value = WXResponse();
        value.errcode= ios.read(tafcore.int32, 0, False, value.errcode);
        value.errmsg= ios.read(tafcore.string, 1, False, value.errmsg);
        return value;

#proxy for client
class SessionObjProxy(ServantProxy):
    def test(self, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "test", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);

        return (ret);

    def ptloginSZKeyVerify(self, head, req, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();
        oos.write(SessionBusiHead, 1, head);
        oos.write(PtloginSZKeyVerifyReq, 2, req);

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "ptloginSZKeyVerify", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);
        rsp = ios.read(PtloginSZKeyVerifyRsp, 3, True);

        return (ret, rsp);

    def oidb0x5e1(self, head, req, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();
        oos.write(SessionBusiHead, 1, head);
        oos.write(Oidb0x5e1Req, 2, req);

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "oidb0x5e1", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);
        rsp = ios.read(Oidb0x5e1Rsp, 3, True);

        return (ret, rsp);

    def wxLoginVerify(self, head, req, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();
        oos.write(SessionBusiHead, 1, head);
        oos.write(WxLoginVerifyReq, 2, req);

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "wxLoginVerify", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);
        rsp = ios.read(WxLoginVerifyRsp, 3, True);

        return (ret, rsp);

    def getXcxSessionKeyByCode(self, head, req, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();
        oos.write(SessionBusiHead, 1, head);
        oos.write(GetXcxSessionKeyByCodeReq, 2, req);

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "getXcxSessionKeyByCode", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);
        rsp = ios.read(GetXcxSessionKeyByCodeRsp, 3, True);

        return (ret, rsp);

    def oidb0x70f(self, req, context = ServantProxy.mapcls_context()):
        oos = tafcore.JceOutputStream();
        oos.write(Oidb0x70fReq, 1, req);

        rsp = self.taf_invoke(ServantProxy.JCENORMAL, "oidb0x70f", oos.getBuffer(), context, None);

        ios = tafcore.JceInputStream(rsp.sBuffer);
        ret = ios.read(tafcore.int32, 0, True);
        rsp = ios.read(Oidb0x70fRsp, 2, True);

        return (ret, rsp);




