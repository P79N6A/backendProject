import random

from lib.config import read_video_url_config
from lib.config import read_cover_url_config
from dao.common import get_video_obj

#user's history
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
            tag    = val['tag']
            weight = val['weight']

            yield (vid, tag, weight)

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
        sql = "select t1.f_id,t1.video_id,t1.timestamp,t1.w_duration,t2.uid,t2.appid,t2.res_url,"\
        "t2.video_id,t2.name,t2.definition,t2.play_count,t2.good_count,t2.duration,"\
        "t2.version,t2.pic_url,t2.src_type,t3.music_ids,"\
        "t4.nickname,t4.user_icon,t5.game_id,t6.content_name,t6.icon_url "\
        "from t_user_videos t1 "\
        "join t_videos t2 on t1.video_id=t2.video_id "\
        "left join t_music_recommend t3 on t2.video_id=t3.video_id "\
        "left join t_open_user_profile t4 on t4.uid=t2.uid "\
        "left join t_video_game t5 on t5.video_id=t2.video_id "\
        "left join t_content t6 on t5.game_id=t6.content_id "\
        "where t1.user_id=%s and t4.uid_type=2 order by t1.timestamp desc"
        for val in self.base.exec_r(sql, self.user):
            uvobj = _UserVideoObj()
            uvobj.f_id       = val['f_id']
            uvobj.user_id    = self.user
            uvobj.video_id   = val['video_id']
            uvobj.timestamp  = val['timestamp']
            uvobj.w_duration = val['w_duration']
            uvobj.game_name  = val['content_name']

            v = get_video_obj(val)
            uvobj.video_obj = v

            yield uvobj

    def get_recommend(self):
        sql = "select video_ids from t_user_recommend where user_id=%s"
        val = self.base.exec_r_one(sql, self.user)
        if val:
            return val['video_ids']
        else:
            return ''

#video uploader and his videos
class UploaderVideo(object):
    def __init__(self):
        pass

    #We only have one video platform now, hero time. 
    #User have a openid in every video platform, so he will have many ids if we have many
    #video platform in future.
    #user_ids present one's openids in whole video platform.
    def get_videos_by_user_ids(self, user_ids=[]):
        if user_ids and len(user_ids):
            chars = ','.join(['%s'] * len(user_ids))
            sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,"\
            "t1.duration,t1.play_count,t1.good_count,t1.version,t1.share_time,t1.appid,t1.uid,t1.appid,t2.category,t3.music_ids,"\
            "t4.nickname,t4.user_icon "\
            "from t_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id "\
            "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
            "left join t_open_user_profile t4 on t4.uid=t1.uid "\
            "where t1.uid in (%s) order by t1.good_count" % chars
            vals = self.base.exec_r(sql, *user_ids)
            for val in vals:
                yield get_video_obj(val)

    def get_videos_by_date(self, date_ts):
        if date_ts:
            sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,"\
            "t1.duration,t1.play_count,t1.good_count,t1.version,t1.share_time,t1.appid,t1.uid,t1.appid,t2.category,t3.music_ids,"\
            "t4.nickname,t4.user_icon "\
            "from t_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id "\
            "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
            "left join t_open_user_profile t4 on t4.uid=t1.uid "\
            "where t1.share_time >= %s and t4.uid_type=2 order by t1.good_count"
            vals = self.base.exec_r(sql, date_ts)
            for val in vals:
                yield get_video_obj(val)


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
        self.game_name  = ''

        self.video_obj = None
