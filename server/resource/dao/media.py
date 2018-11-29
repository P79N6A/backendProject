# -*- coding: UTF-8 -*-

class Media(object):
    def __init__(self, base):
        self.base = base

    def get_all_music(self, user_id):
        result = []
        sql  = """
                  select t1.media_id, t1.player, t1.name, t1.duration, t1.url
                  from t_medias t1
                  where t1.status=1 and t1.type=2 and t1.op_type=1 and t1.user_id=%s order by rand()
               """
        rows = self.base.exec_r(sql, user_id)

        for row in rows:
            music = self._convert_object(row)
            result.append(music)


        sql  = """
                  select media_id, player, name, duration, url
                  from t_medias
                  where status=1 and type=2 and op_type=0 order by rand()
               """
        rows = self.base.exec_r(sql)

        for row in rows:
            music = self._convert_object(row)
            result.append(music)
        return result

    def get_all_video(self, user_id):
        result = []
        sql  = """
                  select t1.media_id, t1.player, t1.name, t1.duration, t1.url, t1.pic_url,
                  t1.play_count,t1.definition,t1.share_time,t1.user_id,
                  t3.nickname,t3.user_icon,t3.rank
                  from t_medias t1
                  left join t_open_user_profile t3 on t3.id=t1.user_id
                  where t1.status=1 and t1.type=3 and t1.op_type=1 and t1.user_id=%s
               """
        rows = self.base.exec_r(sql, user_id)

        for row in rows:
            media = self._convert_object(row)
            result.append(media)

        return result

    def get_all_picture(self, user_id):
        result = []
        sql  = """
                  select t1.media_id, t1.player, t1.name, t1.duration, t1.url, t1.pic_url
                  from t_medias t1
                  where t1.status=1 and t1.type=1 and t1.op_type=1 and t1.user_id=%s
               """
        rows = self.base.exec_r(sql, user_id)

        for row in rows:
            media = self._convert_object(row)
            result.append(media)

        return result

    def get_media_url(self, media_id):
        url = ''

        sql = """
                select url from t_medias where media_id=%s
        """

        rows = self.base.exec_r(sql, media_id)

        if len(rows):
            url = rows[0]['url']

        return url



    def _convert_object(self, row):
        media             = _Media()
        media.no          = row['media_id']
        media.name        = row.get('name') or ''
        media.player      = row.get('player') or ''
        media.time_length = row.get('duration') or 0
        media.url         = row.get('url') or ''
        media.create_time = row.get('create_time') or 0
        media.cover       = row.get('pic_url') or ''
        media.definition  = row.get('definition') or 0
        media.play_count  = row.get('play_count') or 0
        media.share_time  = row.get('share_time') or 0
        media.game_icon   = row.get('game_icon') or ''
        media.userid      = row.get('user_id') or 0 
        media.nickname    = row.get('nickname') or ''
        media.usericon    = row.get('user_icon') or ''
        media.rank        = row.get('rank') or 0
        media.isHD        = media.definition >= 1080
        return media

class _Media(object):
    def __init__(self, no = 0, name = '', player = '', time_length = 0, url = ''):
        self.no          = no
        self.name        = name
        self.player      = player
        self.time_length = time_length
        self.url         = url
        self.create_time = 0
        self.cover       = ''
        self.definition  = 0
        self.play_count  = 0
        self.share_time  = 0
        self.game_icon   = ''
        self.userid      = 0
        self.nickname    = ''
        self.usericon    = ''
        self.rank        = 0
        self.isHD        = False
        self.isMix       = False


    def toDict(self, tp=2):
        dic = {}
        dic['name']        = self.name
        if tp==2:
            dic['singer']  = self.player
            dic['length_time'] = self.time_length
        dic['url']         = self.url
        dic['create_time'] = self.create_time
        dic['cover']       = self.cover
        dic['definition']  = self.definition
        dic['duration']    = self.time_length
        dic['id']          = self.no
        dic['play_count']  = self.play_count
        dic['share_time']  = self.share_time
        dic['title']       = self.name
        dic['url']         = self.url
        dic['game_icon']   = self.game_icon
        dic['userid']      = self.userid
        dic['nickname']    = self.nickname
        dic['usericon']    = self.usericon
        dic['rank']        = self.rank
        dic['isHD']        = self.isHD
        dic['isMix']       = self.isMix

        return dic
