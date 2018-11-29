class MusicTag(object):
    def __init__(self, base):
        self.base = base

    def get_music_id_by_tag(self, tag):
        sql = "select music_id from t_tag_musics where tag=%s"
        val = self.base.exec_r_one(sql, tag)

        if val:
            return val['music_id']

class _MusicTag(object):
    def __init__(self, f_id=0, music_id='0', tag='0'):
        self.f_id     = f_id
        self.music_id = music_id
        self.tag      = tag
