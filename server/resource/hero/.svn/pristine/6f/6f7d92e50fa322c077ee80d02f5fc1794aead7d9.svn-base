import socket
import traceback
import ctypes
from ctypes import *

from hero.struct.sqt_sess_info import SQtSessInfo
from hero.struct.header import *
from hero.struct.udp_conn import getReq
from hero.struct.udp_conn import getResp
from hero.struct.tool import tobytes
from hero.struct.tool import toubyte

class QtHelper(object):
    def __init__(self):
        pass

    def createSessInfo(self,usCmd,ucSubCmd,uiAppid,uin):
        sess          = SQtSessInfo()
        sess.usCmd    = usCmd
        sess.ucSubCmd = ucSubCmd
        sess.uiAppId  = uiAppid
        sess.ulUin    = uin
        #add other
        return sess

    def buildSendPkg(self, sessInfo, pbReq):
        try:
            start_zero = 0
            strReq = pbReq.SerializeToString()
            #strReq = 'test'
            bytesReq = tobytes(strReq, len(strReq))
            oDBPkgHead = DBPkgHead()
            #...
            #usLen = sizeof(DBPkgHead) + sizeof(RelayPkgHeadEx2) + sizeof(CldPkgHead) + sizeof(ctypes.c_ubyte) + len(strReq)
            oDBPkgHead.usLen = sizeof(ReqHeader) + len(bytesReq) + sizeof(c_ubyte)
            #oDBPkgHead.usLen = sizeof(ReqHeader) + len(bytesReq) + sizeof(c_ubyte)
            #0
            c_ushort_htons_sid    = (ctypes.c_ushort)(socket.htons(sessInfo.uiClientType))
            oDBPkgHead.sServerID  = tobytes(c_ushort_htons_sid, 2)
            #0
            c_uint_htons_connaddr = (ctypes.c_uint)(socket.htonl(sessInfo.uiAppId))
            oDBPkgHead.sConnAddr  = tobytes(c_uint_htons_connaddr, 4)


            oRelayPkgHeadEx2         = RelayPkgHeadEx2()
            oRelayPkgHeadEx2.shExLen = sizeof(oRelayPkgHeadEx2)

            oCldPkgHead = CldPkgHead()
            #...
            #0
            c_ushort_ver        = (ctypes.c_ushort)(sessInfo.usVer)
            oCldPkgHead.version = tobytes(c_ushort_ver, 2)
            c_ushort_cmd        = (ctypes.c_ushort)(socket.htons(sessInfo.usCmd))
            oCldPkgHead.command = tobytes(c_ushort_cmd, 2)
            #0
            c_ushort_seq_num    = (ctypes.c_ushort)(sessInfo.usSeq)
            oCldPkgHead.seq_num = tobytes(c_ushort_seq_num, 2)
            #0
            c_uint_uin          = (ctypes.c_uint)(sessInfo.ulUin)
            oCldPkgHead.uin     = tobytes(c_uint_uin, 4)

            cucSubCmd = (ctypes.c_ubyte)(sessInfo.ucSubCmd)

            oReqHeader = ReqHeader()
            oReqHeader.c_a = toubyte(b'\x0a')
            oReqHeader.dBPkgHead = oDBPkgHead
            oReqHeader.relayPkgHeadEx2 = oRelayPkgHeadEx2
            oReqHeader.cldPkgHead = oCldPkgHead
            oReqHeader.subcmd = cucSubCmd

            end = toubyte(b'\x03')

            req = getReq(0, oReqHeader, bytesReq, end)
            return req
            #...


        except:
            print traceback.format_exc()
            print 'error'
        finally:
            pass

    def parseReceivePkg(self, recvBuf):
        try:
            resp = getResp(recvBuf)
            return resp
        except:
            print traceback.format_exc()
        finally:
            pass
