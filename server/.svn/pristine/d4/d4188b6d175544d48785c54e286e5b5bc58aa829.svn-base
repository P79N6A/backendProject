# -*- coding: UTF-8 -*-
import traceback
import random
import httplib
import urllib
import json

from lib.log import get_logger

logger = get_logger('busi')

class Address(object):
    def __init__(self):
        self.__ip   = None
        self.__port = None

    def __def__(self):
        self.__ip   = None
        self.__port = None

    def get_ip(self):
        return self.__ip

    def set_ip(self, value):
        self.__ip = value

    def get_port(self):
        return self.__port

    def set_port(self, value):
        self.__port = value



class DockerRouter(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_router(self, app_name, server_name):
        (ip, port) = ('0.0.0.0', 0)

        request_params = self._make_request_params(app_name, server_name)

        http_client = None
        try:
            http_client = httplib.HTTPConnection('api.sumeru.wsd.com', 80, timeout = 30)
            http_client.request('GET', '/interface?{0}'.format(request_params))

            response = http_client.getresponse()
            if (response.status == 200):
                result     = json.loads(response.read())
                if (result['ret_code'] == 200):
                    (ip, port) = self._random(result)
                else:
                    logger.debug('failure|invoke interface failure|{0}'.format(result['err_msg']))
            else:
                logger.debug('failure|invoke interface failure|{0}'.format(response.reason))
        except:
            logger.error('failure|get router fail|{0}'.format(traceback.format_exc()))
        finally:
            if (http_client):
                http_client.close()

        return (ip, port)

    # env : formal=正式环境 pre=预发布环境 test=业务测试环境
    def _make_request_params(self, app_name, server_name, env = 'test',
                            skey = '3072c68a-cb56-47d2-bec1-0e846878e710', op = 'berlinzhou',
                            interface_name = 'get_router_by_port_type'):
        env_code                = "'env_code':'{0}'".format(env)
        application_name        = "'application_name':'{0}'".format(app_name)
        server_name             = "'server_name':'{0}'".format(server_name)
        port_name               = "'port_name':'main_port'"
        present_state_is_active = "'present_state_is_active':1"
        setting_state_is_active = "'setting_state_is_active':1"

        interface_params = '{{{0},{1},{2},{3},{4},{5}}}'.format(env_code, application_name, server_name,
                                            port_name, present_state_is_active, setting_state_is_active)
        interface_params = urllib.quote(interface_params)

        request_params = 'skey={0}&operator={1}&interface_name={2}&interface_params={3}'.format(skey, op, interface_name, interface_params)

        return request_params

    def _random(self, result_dic):
        array_data = []

        data = result_dic['data']
        for item in data:
            addr = Address()
            addr.set_ip(item['inner_ip'])
            addr.set_port(item['port'])
            array_data.append(addr)
        
        length = len(array_data)
        idx    = random.randint(0, length - 1)

        return (array_data[idx].get_ip(), array_data[idx].get_port())


