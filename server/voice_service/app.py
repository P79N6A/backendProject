# -*- coding: UTF-8 -*-
##################################################################################
# 系统模块
import sys
import logging
import traceback
import time
import urllib
import base64

# 第三方模块
import zerorpc

# 业务自定义模块
from libs.log import get_logger
from service.sng_voice_service import SNGVoiceService
from tools.parser_parameter import ParserParameter

# 日志实例
logger = get_logger('enter')
##################################################################################

##################################################################################
# 语音服务类
class VoiceService(object):
    __sng_voice_service = None
    def __init__(self):
        self.__sng_voice_service = None

    def __del__(self):
        self.__sng_voice_service = None

    def hello(self, name):
        return 'Hello, {0}'.format(name)

    def sng_voice(self, voice_data):
        logger.info('enter a sng voice convert')

        result = False
        try:
            bin_data = base64.b64decode(voice_data)
            if (self.__sng_voice_service.send_request(bin_data) == True):
                result = True
        except:
            logger.critical('error|send voice request failure|{0}'.format(traceback.format_exc()))

        logger.info('end a sng voice convert')
        return result

    def sng_voice_callback(self, request_id, text, audioTime):
        logger.info('enter a sng voice convert callback')

        result = False
        try:
            if (self.__sng_voice_service.receive_result_data(request_id, text, audioTime) == True):
                result = True
        except:
            logger.critical('error|callback voice failure|{0}'.format(traceback.format_exc()))

        logger.info('end a sng voice convert callback')
        return result

    def wx_voice(self, voice_data):
        pass

    def initialize(self):
        self.__sng_voice_service = SNGVoiceService()
        if (self.__sng_voice_service.initialize() == True):
            return True
        return False
##################################################################################

##################################################################################
# 服务初始化和启动
parser_parameter = ParserParameter()
parser_parameter.parser(sys.argv)
host = parser_parameter.get_parameter('host')
port = parser_parameter.get_parameter('port')
bind_address = 'tcp://{0}:{1}'.format(host, port)

voice_service = VoiceService()
if (voice_service.initialize() == False):
    logger.critical('initialize failure|%s' % traceback.format_exc())
    sys.exit(1)
else:
    logger.info('initialize success')

logger.info('app run at {0}'.format(bind_address))
service = zerorpc.Server(voice_service)
service.bind(bind_address)
service.run()
