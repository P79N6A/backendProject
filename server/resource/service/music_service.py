# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.music import Music

logger = get_logger('busi')

class MusicService(object):
    def __init__(self):
        self.__base = None

    def get_music(self):
        self.__base = BaseDao()
        music       = Music(self.__base)
        rows        = music.get_all_music()
        
        arr = []
        for row in rows:
            dic = row.toDict()
            arr.append(dic)
        
        data = {}
        data['musics'] = arr
        data['total']  = len(arr)
        return data

    def close(self):
        if (self.__base is not None):
            self.__base.close()

