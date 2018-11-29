import socket

class UDPClient(object):
    def __init__(self, host='127.0.0.1', port=0, timeout=10):
        self.s    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(timeout)
        self.host = host
        self.port = port

    def sendData(self, host=None, port=None, buf=None):
        if not buf:
            print 'buf is null, return'
            return

        h = host or self.host
        p = port or self.port
        if not (h and p):
            print 'h or p is none'
            return
        address = (h, p)
        self.s.sendto(buf, address)

    def recvData(self, buf_size=None):
        if buf_size:
            data, sender_addr = self.s.recvfrom(buf_size)
            return data
        else:
            buf = []
            while True:
                data, sender_addr = self.s.recvfrom(1024*1024)
                buf.append(data)
                if len(data) < 1024*1024:
                    break
            return ''.join(buf)

    def close(self):
        self.s.close()
