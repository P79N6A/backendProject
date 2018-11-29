from hero.common.enum import enum

class SQtSessInfo(object):
    MAX_RELAY_BUF_LEN = 256
    MAX_USERID_LEN    = 64
    MAX_MATCHINECODE_LEN    = 32

    ReqType = enum(kTCP=1, kUDP=2)

    def __init__(self):
        self.uiAppId = 0
        self.uiClientType = 0
        self.usVer = 0
        self.usSeq = 0
        self.ulUin = 0
        self.usCmd = 0
        self.ucSubCmd = 0
        self.eReqType = SQtSessInfo.ReqType.kUDP
        self.uiClientIp = 0
        self.usClientPort = 0
        self.uiRelayUsedLen = 0
        self.arrRelayBuf = ''


