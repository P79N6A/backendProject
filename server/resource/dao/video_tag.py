class VideoTag(object):
    def __init__(self, base):
        self.base = base

    def set_video_id(self, vid):
        self.vid = vid

    def get_items(self, vid):
        if not vid:
            return
        sql = "select f_id,tag from t_video_tags where video_id=%s"
        for val in self.base.exec_r(sql, vid):
            vt = _VideoTag()
            vt.f_id     = val['f_id']
            vt.video_id = vid
            vt.tag      = val['tag']
            yield vt

    def get_items_by_vid(self, vid):
        sql = "select f_id,tag from t_video_tags where video_id=%s"
        for val in self.base.exec_r(sql, vid):
            vt = _VideoTag()
            vt.f_id     = val['f_id']
            vt.video_id = vid
            vt.tag      = val['tag']
            yield vt

    def get_all_items(self):
        sql = "select t1.f_id,tag,t1.video_id,t1.weight from t_video_tags t1 "\
        "right join t_videos t2 on t2.video_id=t1.video_id"
        for val in self.base.exec_r(sql):
            vt = _VideoTag()
            vt.f_id     = val['f_id']
            vt.video_id = val['video_id']
            vt.tag      = val['tag']
            vt.weight   = val['weight']
            yield vt

class _VideoTag(object):
    def __init__(self, f_id=0, video_id='0', tag='0'):
        self.f_id     = f_id
        self.video_id = video_id
        self.tag      = tag
        self.weight   = 1
