import ctypes
from hero.struct.base_struct import BaseNetStruct
from hero.struct.base_struct import BaseStruct

from acloud.m_struct.define import FTN_UPLOAD_KEY_LEN

class StUploadBody(BaseNetStruct):
    _pack_ = 1
    _fields_ = [
        ('ukey_len', ctypes.c_ushort),
        ('ukey', ctypes.c_byte * FTN_UPLOAD_KEY_LEN),
        ('file_key_len', ctypes.c_ushort),
        ('file_key', ctypes.c_byte * 20),
        ('file_size', ctypes.c_uint),
        ('offset', ctypes.c_uint),
        ('data_len', ctypes.c_uint),
        ('file_sizeH', ctypes.c_uint),
        ('offsetH', ctypes.c_uint)
    ]

class StHttpRsp(BaseNetStruct):
    _pack_ = 1
    _fields_ = [
        ('flag', ctypes.c_byte),
        ('next_offset', ctypes.c_uint),
        ('next_offsetH', ctypes.c_uint)
    ]
