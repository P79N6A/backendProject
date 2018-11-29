# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.user_video import UserVideo
from dao.common import assemble

logger = get_logger('busi')


class HistoryService(object):
    def __init__(self, base=None):
        self.__base = base or BaseDao()

    def close(self):
        if (self.__base is not None):
            self.__base.close()

    def get_chuan_history(self, user_id=''):
        if not user_id:
            logger.error('userid:%s is null'% user_id)
            raise Exception('userid:%s is null'% user_id)

        uv = UserVideo(user = user_id, base = self.__base)
        result = {}
        topic_list = []
        result['tagList'] = topic_list

        obj_all = {}
        topic_list.append(obj_all)
        obj_all['text'] = '全部'
        video_items = []
        obj_all['itemList'] = video_items

        tag_list = {}

        for obj in uv.get_items_obj():
            item = assemble(obj.video_obj)
            video_items.append(item)
            tag_obj = tag_list.setdefault(obj.game_name, {})
            if not (tag_obj.has_key('text') and tag_obj.has_key('itemList')) :
                tag_obj['text'] = obj.game_name
                tag_obj['itemList'] = []

            tag_obj['itemList'].append(item)

        for _,obj in tag_list.iteritems():
            topic_list.append(obj)

        return result

    def add_history(self, user_id=0, video_id='', duration=0):
        import time
        if not (user_id and video_id):
            logger.error('userid:%s or video_id is null'% user_id)
            raise Exception('userid:%s or video_id is null'% user_id)
        ts = int(time.time())
        uv = UserVideo(user = user_id, base = self.__base)
        uv.add_item(user_id, video_id, ts, duration)
