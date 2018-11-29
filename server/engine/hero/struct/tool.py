import ctypes

def tobytes(data, buf_len):
    """Convert a BitArray instance to a ctypes byte array instance"""
    buf = bytearray(data)
    buffer = (ctypes.c_byte * buf_len).from_buffer(buf)
    return buffer

def toubytes(data, buf_len):
    """Convert a BitArray instance to a ctypes byte array instance"""
    buf = bytearray(data)
    buffer = (ctypes.c_ubyte * buf_len).from_buffer(buf)
    return buffer

def toubyte(data):
    """Convert a BitArray instance to a ctypes byte array instance"""
    buf = bytearray(data)
    buffer = (ctypes.c_ubyte).from_buffer(buf)
    return buffer
