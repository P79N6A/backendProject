import threading
import sys
#sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/links')

from service.common import singleton

@singleton
class TimeoutService(object):
    def __init__(self):
        self.timers = {}

    def add_timeout(self, name, time, func):
        if self.timers.has_key(name):
            self.timers[name].cancel()
            self.timers[name] = None

        self.timers[name] = threading.Timer(time, func)
        self.timers[name].start()
    def clear_timeout(self, name):
        if self.timers.has_key(name) and self.timers[name]:
            print 'cancel'
            self.timers[name].cancel()

if __name__ == "__main__":
    import time
    def hello(arg):
        def func():
            print arg
        return func
    timeS = TimeoutService()
    timeS.add_timeout('test', 5, hello('shawn'))
    time.sleep(4)
    print 'hhh'
    TimeoutService().add_timeout('test', 5, hello('shawn2'))
    #timeS.clear_timeout('test')
