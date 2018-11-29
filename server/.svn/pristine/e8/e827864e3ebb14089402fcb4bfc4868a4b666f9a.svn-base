import random
from lib.config import read_video_url_config
from lib.config import read_cover_url_config
from lib.config import read_music_url_config
from dao.common import get_video_obj

class VideoCategory(object):
    def __init__(self, base):
        self.base = base

    def set_video_id(self, vid):
        self.vid = vid

    def get_items_num_by_category(self, category=''):
        sql = "select count(1) as num from t_video_categorys where category=%s"
        count = self.base.exec_r_one(sql, category)
        return count['num']

    def get_items_by_category(self, category='', layer=0, start=0, offset=10):
        sql = "select t1.f_id,t1.video_id from t_video_categorys t1 right join "\
        "t_videos t2 on t1.video_id=t2.video_id where t1.category=%s and t1.layer=%s "\
        "order by t2.create_time DESC,t2.f_id ASC limit %s,%s"
        for val in self.base.exec_r(sql, category, int(layer), start, offset):
            vc = _VideoCategory()
            vc.f_id     = val['f_id']
            vc.video_id = val['video_id']
            vc.layer    = layer
            vc.category = category
            yield vc

    def get_items_by_category2(self, category='', layer=0, start=0, offset=10):
        sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.share_time,"\
        "t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,t1.duration,"\
        "t1.play_count,t1.good_count,t1.version,t1.uid,t1.appid,t2.category,t3.music_ids,"\
        "t4.nickname,t4.user_icon "\
        "from t_video_categorys t2 "\
        "right join t_videos t1 on t2.video_id=t1.video_id "\
        "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
        "left join t_open_user_profile t4 on t4.uid=t1.uid "\
        "where t2.category=%s and t2.layer=%s and t4.uid_type=2"\
        "order by t1.create_time DESC,t1.f_id ASC limit %s,%s"
        for val in self.base.exec_r(sql, category, int(layer), start, offset):
            v = get_video_obj(val)
            yield v


    def get_items_by_vid(self, vid):
        sql = "select f_id,category from t_video_categorys where video_id=%s"
        for val in self.base.exec_r(sql, vid):
            vc = _VideoCategory()
            vc.f_id     = val['f_id']
            vc.video_id = vid
            vc.category = val['category']
            yield vc

    def get_all_items(self, layer=0):
        sql = "select t1.f_id,t1.category,t1.video_id,t2.icon,t3.create_time "\
        "from t_video_categorys t1 left join t_categorys t2 on "\
        "t1.category=t2.name right join t_videos t3 on t1.video_id=t3.video_id where "\
        "t1.layer=%s and t2.status=1 order by t2.f_order ASC,t3.create_time DESC;"
        for val in self.base.exec_r(sql, int(layer)):
            vc = _VideoCategory()
            vc.f_id     = val['f_id']
            vc.video_id = val['video_id']
            vc.category = val['category']
            vc.layer    = layer
            #vc.icon = val['icon']
            vc.icon = vc.category
            #vc.create_time = val['create_time']
            yield vc

    def get_all_categorys(self, layer=0):
        #sql = "select name from t_categorys where layer=%s order by f_order"
        sql = "select name,icon from t_categorys where status=1 order by f_order"
        for val in self.base.exec_r(sql):
            category = val['name']
            icon     = category
            yield (category,icon)

    def get_child_cagegorys_by_category(self, category='', layer=0):
        sql = "select f_c_category from t_category_childrens where"\
        " f_f_category=%s and layer=%s order by f_order"
        for val in self.base.exec_r(sql, category, int(layer)):
            yield val['f_c_category']

class _VideoCategory(object):
    def __init__(self, f_id=0, video_id='0', category='0', icon='0'):
        self.f_id     = f_id
        self.video_id = video_id
        self.category = category
        self.layer    = 0
        self.icon = icon
        #self.create_time = 0
