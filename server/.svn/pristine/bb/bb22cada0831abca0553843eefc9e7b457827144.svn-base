# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.notice import Notice

logger = get_logger('busi')

class NoticeService(object):
    def __init__(self, base=None):
        self.__base = base

    def get_main_notice(self, user_id=0, timestamp=0):
        self.__base = self.__base or BaseDao()
        notice      = Notice(self.__base)
        rows        = notice.get_new_notice(timestamp=timestamp)
        
        arr = []
        for row in rows:
            dic = row.toDict()
            arr.append(dic)
        
        data = {}
        data['notice'] = arr
        data['total']  = len(arr)
        return data


    def close(self):
        if (self.__base is not None):
            self.__base.close()

