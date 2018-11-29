# -*- coding: UTF-8 -*-
import sys
import traceback

from dao.user_video import UserVideo
from dao.video_tag import VideoTag
from dao.base import BaseDao
from dao.video import Video
from lib.config import read_db_config
from lib.log import get_logger

logger = get_logger('busi')

class UserBehavior(object):
    def __init__(self, user='', base=''):
        self.user = user
        if not base:
            base = BaseDao(read_db_config())
        self.base = base

#    def get_behavior(self):
#        if not self.user:
#            print 'need user'
#            return
#
#        try:
#            user_video_dao = UserVideo(self.user, self.base)
#            video_tag_dao  = VideoTag(self.base)
#            user_videos = user_video_dao.get_items()
#            for uv in user_videos:
#                vid = uv.video_id
#		#print '@@@@', vid
#                video_tags = video_tag_dao.get_items(vid)
#                for vt in video_tags:
#                    tag = vt.tag
#                    #print tag.encode('utf-8')
#                    yield (self.user, vid, tag)
#
#        except Exception as e:
#            print e
#        finally:
#            pass
#            #self.base.close()

    def get_behavior(self):
        if not self.user:
            logger.warn('need user, return')
            return
        try:
            user_video_dao = UserVideo(self.user, self.base)
            for vid,tag,weight in user_video_dao.get_vid_and_tags():
                yield (self.user, vid, tag, weight)

        except:
            logger.error('fail|exception|get_behavior error|%s' % traceback.format_exc())
        finally:
            pass
            #self.base.close()

    def get_all_items(self):
        try:
            video_tag_dao  = VideoTag(self.base)
            video_tags = video_tag_dao.get_all_items()
            for vt in video_tags:
                yield (vt.video_id, vt.tag, vt.weight)

        except:
            logger.error('fail|exception|get_behavior error|%s' % traceback.format_exc())
        finally:
            pass
            #self.base.close()

    def del_video_history(self, vid):
        uv = UserVideo(self.user, self.base)
        uv.del_item(vid=vid)

    def del_all_video_history(self):
        uv = UserVideo(self.user, self.base)
        uv.del_all_item()

    def get_recommend(self):
        uv = UserVideo(self.user, self.base)
        return uv.get_recommend()

    def close(self):
        self.base.close()

if __name__ == '__main__':
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    ub = UserBehavior('shawnsha')
    for d in ub.get_behavior():
        print ','.join(d).encode('utf-8')
