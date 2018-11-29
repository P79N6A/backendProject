# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.tags import Tag

logger = get_logger('busi')

class TagService(object):
    def __init__(self):
        self.__base = None

    def get_tag_by_content(self, content = 'unknown'):
        self.__base   = BaseDao()
        op            = Tag(self.__base)
        (total, rows) = op.get_tags_by_content(content)
        
        result = []
        for row in rows:
            dic = row.toDict()
            result.append(dic)
        
        data = {}
        data['contents'] = result
        data['total']    = total
        return data

    def get_all_content(self):
        self.__base   = BaseDao()
        op            = Tag(self.__base)
        (total, rows) = op.get_all_content()
        
        result = []
        for row in rows:
            dic = row.toDict()
            result.append(dic)
        
        data = {}
        data['contents'] = result
        data['total']    = total
        return data


    def close(self):
        if (self.__base is not None):
            self.__base.close()

