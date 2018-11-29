# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
#from dao.music import Music
from dao.media import Media

logger = get_logger('busi')

class MediaService(object):
    def __init__(self):
        self.__base = None

    def get_music(self, user_id):
        self.__base = BaseDao()
        music       = Media(self.__base)
        rows        = music.get_all_music(user_id)
        
        arr = []
        for row in rows:
            dic = row.toDict(tp=2)
            arr.append(dic)
        
        data = {}
        data['musics'] = arr
        data['total']  = len(arr)
        return data

    def get_video(self, user_id):
        self.__base = BaseDao()
        media       = Media(self.__base)
        rows        = media.get_all_video(user_id)
        
        arr = []
        for row in rows:
            dic = row.toDict(tp=3)
            arr.append(dic)
        
        data = {}
        data['videos'] = arr
        data['total']  = len(arr)
        return data

    def get_picture(self, user_id):
        self.__base = BaseDao()
        media       = Media(self.__base)
        rows        = media.get_all_picture(user_id)
        
        arr = []
        for row in rows:
            dic = row.toDict(tp=1)
            arr.append(dic)
        
        data = {}
        data['pictures'] = arr
        data['total']  = len(arr)
        return data


    def close(self):
        if (self.__base is not None):
            self.__base.close()

