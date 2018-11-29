# -*- coding: UTF-8 -*-
import sys
import traceback
from dao.base import BaseDao
from dao.user_video import UserVideo
from dao.user_recommend import UserRecommender
from lib.config import read_db_config
from lib.tag_recommand import get_rec_list
from lib.music_recommand import rec_music
from lib.log import get_logger

logger = get_logger('busi')
video_logger = get_logger('video')
music_logger = get_logger('music')

class Recommender(object):
    def __init__(self,num=50):
        self.base = BaseDao(read_db_config())
        self.num = num

    def recommend(self):
        uv = UserVideo(base=self.base)
        ur = UserRecommender(base=self.base)
        for user_id in uv.get_all_users():
            video_logger.info('start rec video of user_id:%s' % user_id)
            items = []
            for k,v in get_rec_list(self.num, user_id):
                items.append(k)
            if len(items):
                rec_list_str = ','.join(items)
                video_logger.info('add user:%s recommend:%s'%(user_id, rec_list_str))
                ur.add_recommend(user_id, rec_list_str)
            video_logger.info('finish rec user_id:%s' % user_id)

    def music_recommend(self):
        music_logger.info('start music recommend')
        rec_music(self.base)
        music_logger.info('finish music recommend')

    def close(self):
        self.base.close()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    rec = Recommender()
    rec.recommend()
