import ctypes
from hero.struct.base_struct import BaseStruct
from hero.struct.header import ReqHeader

def getReq(start, header, body, end):
    class UDPReq(BaseStruct):
        _pack_ = 1
        _fields_ = [
            #('start', ctypes.c_ushort),
            ('header', ReqHeader),
            ('body_str', ctypes.c_byte * len(body)),
            ('c_end', ctypes.c_ubyte)
        ]

        def __init__(self, start, header, body, end):
            #print repr(start)
            #print repr(end)
            #self.start  = start
            self.header = header
            self.body_str = body
            self.c_end    = end
            #self.receiveSome(self.send())
            #self.receiveSome(start + header.send() + body + end)

        def serialize(self):
            return buffer(self)[:]

        def unserialize(self, bs):
            fit = min(len(bs), ctypes.sizeof(self))
            ctypes.memmove(ctypes.addressof(self), bs, fit)

    return UDPReq(start, header, body, end)

def getResp(resp_buf):
    body_len = len(resp_buf) - ctypes.sizeof(ReqHeader) - ctypes.sizeof(ctypes.c_ubyte)

    class UDPResp(BaseStruct):
        _pack_ = 1
        _fields_ = [
            ('header', ReqHeader),
            ('body_str', ctypes.c_byte * body_len),
            ('c_end', ctypes.c_ubyte)
        ]

        def __init__(self, buf):
            self.buf = buf

        def serialize(self):
            return buffer(self)[:]

        def unserialize(self):
            fit = min(len(self.buf), ctypes.sizeof(self))
            ctypes.memmove(ctypes.addressof(self), self.buf, fit)

    return UDPResp(resp_buf)
