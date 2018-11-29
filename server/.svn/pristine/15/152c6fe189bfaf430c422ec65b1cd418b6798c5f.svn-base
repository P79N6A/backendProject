#-*- coding:utf-8 -*-

# 命令行参数解析器
class ParserParameter(object):

    # 执行的命令
    __script    = ""
    # 执行命令输入的参数
    __parameter = {}

    def __init__(self):
        self.__script    = ""
        self.__parameter = {}

    def __del__(self):
        self.__script    = ""
        self.__parameter = {}

    # 获取执行的命令
    def get_script(self):
        return self.__script

    # 根据指定参数名取值
    def get_parameter(self, name):
        key = "--" + name
        if (key in self.__parameter.keys()):
            return self.__parameter[key]
        else:
            return None

    # 解析命令行参数
    def parser(self, argv):
        self.__script = argv[0]
        for (idx, val) in enumerate(argv):
            if idx == 0:
                continue
            array                      = val.split("=")
            self.__parameter[array[0]] = array[1]

    # 显示解析的结果
    def display(self):
        print("execute script : " + self.get_script())
        for key in self.__parameter:
            print(key + "=" + self.__parameter[key])
