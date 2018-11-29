# -*- coding: UTF-8 -*-
import traceback

from dao.base import BaseDao
from dao.video import Video
from lib.log import get_logger

logger = get_logger('main')

class ChuanService(object):
 
    def __init__(self, base=None):
        self.b = base or BaseDao()
        self.video_dao = Video(self.b)

    def close(self):
        if self.b:
            self.b.close()
            self.b = None

    def query_title(self, uid=0, vids=[]):
        data = {'title':[]}
        title = data['title']
        title.append('精彩串烧视频')
        if not (vids and len(vids)):
            logger.error('vids is null')
            raise Exception('vidss is null')

        game_names = []
        for vid in vids:
            name = self.video_dao.get_second_c_by_vid(vid)
            if name:
                game_names.append(name)

        if len(game_names):
            title.append('-'.join(game_names))

        nickname = self.video_dao.get_nickname_by_vid(uid)
        if not nickname:
            nickname = '我'

        name = nickname + '的精彩串烧视频'

        title.append(name)

        return data

