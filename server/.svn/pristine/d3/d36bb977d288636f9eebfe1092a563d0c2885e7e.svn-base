import random
from lib.config import read_video_url_config
from lib.config import read_cover_url_config

class Video(object):
    def __init__(self, base):
        self.base = base

    def get_info_by_vid(self, vid):
        sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,t1.duration,t1.play_count,t1.good_count,t1.version,t2.category from t_videos t1 left join t_video_categorys t2 on t1.video_id = t2.video_id where t1.video_id=%s"
        vals = self.base.exec_r(sql, vid)
        if vals:
            val = vals[0]
            v = _Video()
            v.f_id = val['f_id']
            v.video_id = val['video_id']
            v.name = val['name']
            v.definition = val['definition']
            v.category   = val['category']
            v.play_count = val['play_count'] if val['play_count'] != 0 else random.randint(1,10)
            v.good_count = val['good_count'] if val['good_count'] != 0 else random.randint(1,10)
            v.version    = val['version']
            v.src_type   = val['src_type']
            v.create_time = val['create_time']
            v.url        = val['res_url']
            v.cover      = val['pic_url']
            v.url   = read_video_url_config(v)
            v.cover = read_cover_url_config(v)
            v.duration    = val['duration']
            return v

    def add_play_count(self, vid):
        sql = 'update t_videos set play_count=play_count+1 where video_id=%s'
        self.base.exec_w(sql, vid)

    def add_good_count(self, vid):
        sql = 'update t_videos set good_count=good_count+1 where video_id=%s'
        self.base.exec_w(sql, vid)

class _Video(object):
    def __init__(self, f_id=0, video_id=0, name='', definition='', url='',
                 cover='',category='',play_count=100000,good_count=10000,
                 duration=0.0):
        self.f_id = f_id
        self.video_id = video_id
        self.name = name
        self.definition = definition
        self.url   = url
        self.cover = cover
        self.play_count = play_count
        self.good_count = good_count
        self.category   = category
        self.duration   = duration
        self.version    = 'v100'
        self.create_time = 0
