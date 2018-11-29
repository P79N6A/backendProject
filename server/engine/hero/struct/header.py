from ctypes import *
import ctypes
#from hero.struct.base_struct import BaseNetStruct
from hero.struct.base_struct import BaseNetStruct

class DBPkgHead(BaseNetStruct):
    #27
    _pack_ = 1
    _fields_ = [
        ('usLen',     c_uint16),
        ('cCommand',  c_uint8),
        ('sServerID', c_byte * 2),
        ('sClientAddr', c_byte * 4),
        ('sClientPort', c_byte * 2),
        ('sConnAddr', c_byte * 4),
        ('sConnPort', c_byte * 2),
        ('sInterfaceAddr', c_byte * 4),
        ('sInterfacePort', c_byte * 2),
        ('cProcessSeq', c_byte),
        ('cDbID',       c_uint8),
        ('sPad',        c_byte * 2)
    ]

class RelayPkgHeadEx2(BaseNetStruct):
    #9
    _pack_ = 1
    _fields_ = [
        ('shExVer', c_uint16),
        ('shExLen', c_uint16),
        ('shLocaleID', c_uint16),
        ('shTimeZoneOffsetMin', c_short),
        ('sReserved', c_byte)
    ]

class CldPkgHead(BaseNetStruct):
    #10
    _pack_ = 1
    _fields_ = [
        ('version', c_byte * 2),
        ('command', c_byte * 2),
        ('seq_num', c_byte * 2),
        ('uin', c_byte * 4)
    ]

class ReqHeader(BaseNetStruct):
    #48
    _pack_ = 1
    _fields_ = [
        ('c_a', c_ubyte),
        ('dBPkgHead', DBPkgHead),
        ('relayPkgHeadEx2', RelayPkgHeadEx2),
        ('cldPkgHead', CldPkgHead),
        ('subcmd', c_ubyte)
    ]
