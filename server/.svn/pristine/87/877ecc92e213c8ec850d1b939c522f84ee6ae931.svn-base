# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.user_profile import UserProfile
from dao.video import Video

logger = get_logger('busi')

class WatchService(object):
    def __init__(self, base=None):
        self.__base = base

    def get_watch_all(self, user_id = 0):
        self.__base   = self.__base or BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_watch_by_user_all(user_id)

        result   = []
        for row in rows:
            result.append(row.no)

        return result



    def get_watch(self, user_id = 0, page_num = 0, page_size = 10):
        self.__base   = BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_watch_by_user(user_id, 30, page_num)

        is_big_v = False
        result   = []
        for row in rows:
            u = row.toDict()
            u['is_big_v'] = is_big_v
            result.append(u)
 
        data             = {}
        data['users']    = result
        data['total']    = len(rows)
        return data

    def get_watch_videos(self, user_id, page_num):
        self.__base   = BaseDao()
        video         = Video(self.__base)
        watch_users   = self.get_watch_all(user_id = user_id)
        (total, rows) = video.get_video_by_users(page_num=page_num, page_size=30, user_ids=watch_users)

        data            = {}
        videos = []
        data['videos']  = videos
        data['total']   = len(rows)
        for row in rows:
            videos.append(row.toDict())
        return data


    def get_fans(self, user_id = 0, page_num = 0, page_size = 10):
        self.__base   = BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_fans_by_user(user_id, page_size, page_num)

        is_big_v = False
        result   = []
        for row in rows:
            u = row.toDict()
            
            u['is_big_v'] = is_big_v
            if (is_big_v):
                is_big_v = False
            else:
                is_big_v = True
            
            (play_count, icons)   = op.get_user_content(u['userid'])
            u['total_play_count'] = play_count
            u['games']            = icons
            
            result.append(u)
        
        data           = {}
        data['fans']   = result
        data['total']  = total
        return data

    def watch(self, watch_id, watched_id, status):
        self.__base = BaseDao()
        op          = UserProfile(self.__base)
        op.watch(watch_id, watched_id, status)

        data              = {}
        data['op_result'] = '成功'
        return data

    def is_watch(self, userid1, userid2):
        self.__base = BaseDao()
        op          = UserProfile(self.__base)
        return op.is_watch(userid1, userid2)

    def user_watch_relation(self, userid1, userid2):
        data = {}
        data['is_watch'] = self.is_watch(userid1, userid2)
        return data

    def _get_message(self):
        dic            = {}
        dic['praise']  = 3
        dic['watch']   = 8
        dic['cluster'] = 6
        dic['system']  = 2
        return dic
        
    def close(self):
        if (self.__base is not None):
            self.__base.close()
            self.__base = None

