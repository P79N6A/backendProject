# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.category import Category

from lib.config import read_icon_url_config
from lib.config import read_icon_url_f_config
from lib.config import read_icon_url_s_config

logger = get_logger('busi')

class CategoryService(object):
    def __init__(self):
        self.__base = None

    def get_categorys(self):
        self.__base = BaseDao()
        op          = Category(self.__base)
        rows        = op.get_all_category()
        
        data = []
        for row in rows:
            item = {}
            item['text']       = row.name
            item['type']       = row.c_type
            item['type_id']    = row.type_id
            item['url']        = read_icon_url_config(row.name)
            item['url_focus']  = read_icon_url_f_config(row.name)
            item['url_select'] = read_icon_url_s_config(row.name)
            data.append(item)
        
        result         = {}
        result['navs'] = data
        return result

    def close(self):
        if (self.__base is not None):
            self.__base.close()

