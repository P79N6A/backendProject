import random

from lib.config import read_video_url_config
from lib.config import read_cover_url_config
from lib.log import get_logger
logger = get_logger('busi')

class UserVideo(object):
    def __init__(self, user='', base=None):
        self.user = user
        self.base = base

    def set_user_id(self, user):
        self.user = user

    def get_items(self):
        sql = "select f_id,video_id,timestamp,w_duration from t_user_videos where user_id=%s order by timestamp desc"
        for val in self.base.exec_r(sql, self.user):
            uv = _UserVideo()
            uv.f_id = val['f_id']
            uv.user_id = self.user
            uv.video_id = val['video_id']
            uv.timestamp = val['timestamp']
            uv.w_duration = val['w_duration']

            yield uv


    #def get_vid_and_category(self):
    #    sql = "select t1.video_id,t2.tag from t_user_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id where t1.user_id=%s"
    #    for val in self.base.exec_r(sql, self.user):
    #        vid = val['video_id']
    #        tag = val['tag']

    #        yield (vid, tag)

    def get_vid_and_tags(self):
        sql = "select t1.video_id,t2.tag,t2.weight from t_user_videos t1 left join t_video_tags t2 on t1.video_id=t2.video_id where t1.user_id=%s"
        for val in self.base.exec_r(sql, self.user):
            vid    = val['video_id']
            if not vid:
                logger.warn('[WARN]user_id:%s has no vid item in t_user_videos'%self.user)
                continue
            tag    = val['tag']
            weight = val['weight']

            if tag and weight:
                yield (vid, tag, weight)
            else:
                logger.warn('[WARN]vid:%s has no tag or weight item in t_video_tags'%vid)

    def add_item(self, uid, vid, tt, duration):
        sql = "replace into t_user_videos(user_id, video_id, timestamp,w_duration) values (%s,%s, %s, %s)"
        self.base.exec_w(sql,uid, vid, int(tt), int(duration))

    def del_item(self, uid='', vid=''):
        user_id = uid or self.user
        if not vid:
            raise Exception('need vid')
            return
        sql = "delete from t_user_videos where user_id=%s and video_id=%s"
        self.base.exec_w(sql, user_id, vid)

    def del_all_item(self, uid=''):
        user_id = uid or self.user
        sql = "delete from t_user_videos where user_id=%s"
        self.base.exec_w(sql, user_id)

    def get_items_obj(self):
        sql = "select t1.f_id,t1.video_id,t1.timestamp,t1.w_duration,t2.res_url,"\
        "t2.video_id,t2.name,t2.definition,t2.play_count,t2.good_count,t2.duration,"\
        "t2.version,t2.pic_url,t2.src_type from t_user_videos t1 right join t_videos t2 on "\
        "t1.video_id=t2.video_id where t1.user_id=%s order by t1.timestamp desc"
        for val in self.base.exec_r(sql, self.user):
            uvobj = _UserVideoObj()
            uvobj.version    = val['version']
            uvobj.f_id       = val['f_id']
            uvobj.user_id    = self.user
            uvobj.video_id   = val['video_id']
            uvobj.timestamp  = val['timestamp']
            uvobj.w_duration = val['w_duration']

            uvobj.definition = val['definition']
            uvobj.name       = val['name']
            uvobj.duration   = val['duration']
            uvobj.src_type   = val['src_type']
            #v.create_time    = val['create_time']
            uvobj.url        = val['res_url']
            uvobj.cover      = val['pic_url']
            uvobj.url   = read_video_url_config(uvobj)
            uvobj.cover = read_cover_url_config(uvobj)
            uvobj.duration  = val['duration']
            uvobj.play_count = val['play_count'] if val['play_count'] != 0 else random.randint(1,10)
            uvobj.good_count = val['good_count'] if val['good_count'] != 0 else random.randint(1,10)

            yield uvobj

    def get_recommend(self):
        sql = "select video_ids from t_user_recommend where user_id=%s"
        val = self.base.exec_r_one(sql, self.user)
        if val:
            return val['video_ids']
        else:
            return ''

    def get_all_users(self):
        sql = "select user_id from t_user_videos group by user_id"
        for val in self.base.exec_r(sql):
            user_id = val['user_id']
            yield user_id


class _UserVideo(object):
    def __init__(self, f_id=0, user_id='0', video_id='0',timestamp=0,w_duration=0):
        self.f_id     = f_id
        self.user_id  = user_id
        self.video_id = video_id
        self.timestamp = timestamp
        self.w_duration = w_duration

class _UserVideoObj(object):
    def __init__(self, f_id=0, user_id='0',
                 video_id='0',timestamp=0,w_duration=0,play_count=0,good_count=0):
        self.f_id     = f_id
        self.user_id  = user_id
        self.video_id = video_id
        self.timestamp = timestamp
        self.w_duration = w_duration

        self.name = ''
        self.duration = 0
        self.definition = 0
        self.url = ''
        self.cover = ''
        self.play_count = play_count
        self.good_count = good_count
