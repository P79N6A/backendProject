# -*- coding: UTF-8 -*-
# 语音转文字接口文档
# https://cloud.tencent.com/document/product/441/6201
import sys
import time
import datetime
import hmac
import hashlib
import base64
import random
import logging
import traceback
import urllib
import logging

import json
import requests

from libs.log import get_logger
from libs.config import init_sng_voice_config

logger = get_logger('sng')


class SNGVoiceService(object):
    def __init__(self):
        self.__base = None
        self.__request_ids = {}

    def __del__(self):
        self.__request_ids = {}
        self.__request_ids = None

    def initialize(self):
        try:
            self.__conf = init_sng_voice_config()
        except:
            logger.critical('initialize sng congfig failure, please check congfig|{0}'.format(traceback.format_exc()))
            return False
        finally:
            logger.debug('initialize sng congfig success')
            return True

    # 处理客户端传来的语音数据，并将数据处理后提交给腾讯云平台
    def send_request(self, voice_data):
        app_id     = self.__conf['appid']
        project_id = self.__conf['projectid']
        secret_id  = self.__conf['secretid']
        secret_key = self.__conf['secretkey']
        orig_url   = self.__conf['url']
        cb_url     = self.__conf['cb_url']

        params      = self._get_request_parameter(project_id, cb_url, secret_id)
        request_url = self._make_request_url(orig_url, app_id, params)
        header      = self._get_request_header(request_url, secret_key)

        logger.info('request url => {0}'.format(request_url))
        logger.info('header => {0}'.format(header))
        response = requests.post(request_url, headers = header, data = voice_data, verify = False)

        if (response.status_code != 200):
            logger.error('request failure, return code [{0}], message [{1}]'.format(response.status_code, response.text))
            return False

        text_dic = json.loads(response.text)
        if (text_dic['code'] != 0):
            logger.error('request failure|return code[{0}]|return message[{1}]'.format(text_dic['code'], text_dic['message']))
            return False

        # 记录请求id，为callback做准备，在这里可以记录一些请求信息
        logger.info('request success|request id [{0}]'.format(text_dic['requestId']))
        id_string = '{0}'.format(text_dic['requestId'])
        self.__request_ids[id_string] = 1
        return True

    # 接收腾讯云平台回调url的数据
    def receive_result_data(self, request_id, text, audio_time):
        logger.info('request id => {0}|text = > {1}|time length => {2}'.format(request_id, text.encode('utf-8'), audio_time))

        id_string = '{0}'.format(int(request_id))
        if (self.__request_ids.has_key(id_string) == True):
            del self.__request_ids[id_string]
            logger.info('delete request id [{0}] data'.format(request_id))

        return True

    def _make_request_url(self, url, app_id, params):
        param_string = self._dict_to_string(params)
        request_url  = '{0}/{1}?{2}'.format(url, app_id, param_string)
        return request_url

    def _get_request_parameter(self, project_id, cb_url, secret_id):
        params = {
                'projectid': 0,
                'sub_service_type': 0,
                'engine_model_type': 1,
                'res_text_format': 0,
                'res_type': 1,
                'callback_url': 'http://test.qq.com/rec_callback',
                'source_type': 0,
                'secretid': 'AKIDUfLUEUigQiXqm7CVSspKJnuaiIKtxqAv',
                'timestamp': 1473752207,
                'expired': 1473752807,
                'nonce': 44925,
            }

        dtime     = datetime.datetime.now()
        timestamp = int(time.mktime(dtime.timetuple()))
        expired   = timestamp + 3600

        params['projectid']    = project_id
        params['callback_url'] = cb_url
        params['source_type']  = 1
        params['secretid']     = secret_id
        params['nonce']        = random.randint(100000, 200000)
        params['timestamp']    = timestamp
        params['expired']      = expired

        return params

    def _dict_to_string(self, dic):
        tmp_string = ''

        sort_key = sorted(dic.keys())
        
        for key in sort_key:
            tmp_string = tmp_string + '{0}={1}&'.format(key, dic[key])

        return tmp_string.rstrip('&')

    def _get_request_header(self, request_url, secret_key):
        header = {
                'Content-Type': 'application/octet-stream',
                'Authorization': 'UyKZ+Q4xMbdu3gxOmPD7tgnAm1A='
            }

        # 签名原文前的https://需要替换为POST在做签名
        sig_str   = request_url.replace('https://', 'POST', 1)
        signature = hmac.new(secret_key, sig_str, hashlib.sha1).digest()
        signature = base64.b64encode(signature).rstrip()

        header['Authorization'] = signature
        return header


