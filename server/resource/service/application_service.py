# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.application import Application

logger = get_logger('busi')

class ApplicationService(object):
    def __init__(self):
        self.__base = None

    def get_all_app(self):
        self.__base = BaseDao()
        app         = Application(self.__base)
        rows        = app.get_all_app()
        
        data = {}
        for row in rows:
            data[row.appid] = row.toDict()
        return data

    def close(self):
        if (self.__base is not None):
            self.__base.close()

