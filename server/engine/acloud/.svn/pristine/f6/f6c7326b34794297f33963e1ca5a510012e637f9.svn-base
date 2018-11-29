import ctypes
from hero.struct.base_struct import BaseNetStruct
from hero.struct.base_struct import BaseStruct

class C_e(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('cmd', ctypes.c_uint),
        ('error', ctypes.c_int)
    ]


class StHeader(BaseStruct):
    _pack_ = 1
    _anonymous_ = ('c_e',)
    _fields_ = [
        ('magic_num', ctypes.c_uint),
        ('c_e', C_e),
        ('reserved', ctypes.c_uint),
        ('body_len', ctypes.c_uint)
    ]
