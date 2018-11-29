"""
author: shawnsha@tencent.com
date: 2016.08.11

Static Factory to generate submodule.
"""


class Factory(object):
    def __new__(cls, *args, **kwargs):
        base = cls.config_base()
        if base is cls:
            impl = cls.config_sub()
        else:
            impl = cls
        
        #Generate concrete class through config_sub.
        instance = super(Factory, cls).__new__(impl)

        instance.__init__(*args, **kwargs)

        return instance

    @classmethod
    def config_base(cls):
        raise NotImplementedError()

    @classmethod
    def config_sub(cls):
        raise NotImplementedError()

    @classmethod
    def config(cls):
        raise NotImplementedError()
    
    @classmethod
    def produce(cls, *args, **kwargs):
        return cls.__new__(cls, *args, **kwargs) 

class TestFactory(Factory):
    name = '1'

    @classmethod
    def config_base(cls):
        return TestFactory

    @classmethod
    def config_sub(cls):
        return Map.get(cls.name)
        #if cls.name == '1':
        #    return Test1
        #else:
        #    print '22222'
        #    return Test2

    @classmethod
    def config(cls, name):
        cls.name = name
        return cls


class Test1(object):
    def __init__(self):
        pass

    def hello(self):
        print 'hello1'


class Test2(object):
    def __init__(self):
        pass

    def hello(self):
        print 'hello2'

Map = {
    '1' : Test1,
    '2' : Test2
}

if __name__ == "__main__":
    obj = TestFactory.config('1').produce()
    #obj = TestFactory.produce()
    obj.hello()
