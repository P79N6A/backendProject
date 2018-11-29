import ctypes

class BaseStruct(ctypes.Structure):
    #def __new__(cls, socket_buffer=None, req=None):
    #    if socket_buffer:
    #        return cls.from_buffer_copy(socket_buffer)
    #    else:
    #        return ctypes.BigEndianStructure.__new__(cls)

    def serialize(self):
        return buffer(self)[:]

    def unserialize(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)

class BaseNetStruct(ctypes.BigEndianStructure):
    #def __new__(cls, socket_buffer=None, req=None):
    #    if socket_buffer:
    #        return cls.from_buffer_copy(socket_buffer)
    #    else:
    #        return ctypes.BigEndianStructure.__new__(cls)

    def serialize(self):
        return buffer(self)[:]

    def unserialize(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)
