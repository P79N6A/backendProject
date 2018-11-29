import ctypes
from hero.struct.base_struct import BaseStruct
from acloud.m_struct.header import StHeader
from acloud.m_struct.body import StUploadBody
from acloud.m_struct.body import StHttpRsp
from common.tool import tobytes

def getReq(stheader, stbody, buf):
    class HTTPReq(BaseStruct):
        _pack_ = 1
        _fields_ = [
            #('start', ctypes.c_ushort),
            ('stheader', StHeader),
            ('stbody', StUploadBody),
            ('body_str', ctypes.c_byte * len(buf))
        ]

        def __init__(self, stheader, stbody, buf):
            self.stheader = stheader
            self.stbody   = stbody
            self.body_str = tobytes(buf, len(buf))

        def serialize(self):
            return buffer(self)[:]

        def unserialize(self, bs):
            fit = min(len(bs), ctypes.sizeof(self))
            ctypes.memmove(ctypes.addressof(self), bs, fit)

    return HTTPReq(stheader, stbody, buf)

def getResp(resp_buf):
    class HTTPResp(BaseStruct):
        _pack_ = 1
        _fields_ = [
            ('stheader', StHeader),
            ('sthttpRsp', StHttpRsp)
        ]

        def __init__(self, buf):
            self.buf = buf

        def serialize(self):
            return buffer(self)[:]

        def unserialize(self):
            fit = min(len(self.buf), ctypes.sizeof(self))
            ctypes.memmove(ctypes.addressof(self), self.buf, fit)

    return HTTPResp(resp_buf)
