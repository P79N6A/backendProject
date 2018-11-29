# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
#from dao.music import Music
from dao.dance import Dance

logger = get_logger('busi')

class DanceService(object):
    def __init__(self, base=None):
        self.__base = base or BaseDao()

    def share_dance_grade(self, dance_id=0):
        data = {}
        dance        = Dance(self.__base)
        work_obj     = dance.get_work_by_dance_id(dance_id=dance_id)
        work_id      = work_obj.id
        if not work_id:
            return data

        grade_detail = dance.get_grade_detail(dance_id=dance_id, work_id=work_id)

        dancers      = dance.get_dancers_by_work_id(work_id=work_obj.id, tp=1)

        dancer_infos = []
        for d in dancers:
            dancer_infos.append(d.toDict())

        data['grade_detail'] = grade_detail
        data['video_info']   = work_obj.toDict()
        data['rand_list']    = dancer_infos
        return data


    def get_dance_music(self, tp=0):
        dance       = Dance(self.__base)
        rows        = dance.get_all_dance_music(tp=tp)

        arr = []
        for row in rows:
            music_id    = row.music_id
            dancers     = self._get_dancers_by_music_id(music_id)
            row.dancers = dancers
            dic = row.toDict()
            arr.append(dic)

        data = {}
        data['data'] = arr
        data['total']  = len(arr)
        return data

    def get_works_by_music_id(self, music_id='', tp=0):
        dance       = Dance(self.__base)
        rows        = dance.get_works_by_music_id(music_id=music_id, tp=tp)

        arr = []
        for row in rows:
            dic = row.toDict()
            arr.append(dic)

        data = {}
        data['data'] = arr
        data['total']  = len(arr)
        return data

    def get_dancers_by_music_id(self, music_id):
        dancers = self._get_dancers_by_music_id(music_id)
        arr = []
        for dancer in dancers:
            dic = dancer.toDict()
            arr.append(dic)

        data = {}
        data['data'] = arr
        data['total']  = len(arr)
        return data


    def get_dancers_by_work_id(self, work_id=0, dance_id=0, tp=0, user_id=0):
        from dao.user_profile import UserProfile
        dance        = Dance(self.__base)
        user_dao     = UserProfile(self.__base)
        if not work_id:
            work_obj = dance.get_work_by_dance_id(dance_id=dance_id)
            work_id  = work_obj.id
            user_id  = user_id or work_obj.user_id

        followings   = user_dao.get_all_followings(user_id)
        follow_ids   = [user.no for user in followings]

        rows         = dance.get_dancers_by_work_id(work_id=work_id, tp=tp)

        arr = []
        for row in rows:
            dic = row.toDict()
            dic['isWatch'] = False
            if row.user_id in follow_ids:
                dic['isWatch'] = True
            arr.append(dic)


        data = {}
        data['data']    = arr
        data['total']   = len(arr)
        if dance_id:
            dancer         = dance.get_dancer_by_dance_id(dance_id=dance_id, work_id=work_id)
            data['myself'] = dancer.toDict()
        return data

    def _get_dancers_by_music_id(self, music_id):
        dance       = Dance(self.__base)
        dancers     = dance.get_dancers_by_music_id(music_id)

        return dancers

    def add_work_dancer(self, user_id=0, work_id=0, score=0, duration=0):
        import time
        dance       = Dance(self.__base)
        dance_id    = dance.add_work_dancer(user_id=user_id, work_id=work_id, score=score,
                                            duration=duration, ts=int(time.time()))

        data = {}
        data['dance_id'] = dance_id
        return data

    def get_work_data(self, work_id=0):
        dance    = Dance(self.__base)
        dance_data     = dance.get_work_data(work_id=work_id)

        data = {}
        data['data']   = dance_data
        data['length'] = len(dance_data)
        return data

    def close(self):
        if (self.__base is not None):
            self.__base.close()
