# -*- coding: UTF-8 -*-

class Dance(object):
    def __init__(self, base):
        self.base = base

    def get_all_dance_music(self, tp=0):
        order_map = {
            0 : "create_time",
            1 : "play_count"
        }

        order_tp = order_map[tp]
        result = []
        sql  = """
                  select count(1) as play_count, t1.id, t1.music_id, t1.name, t1.player, t1.duration,
                  t1.high_duration, t1.url, t1.create_time, t1.pic_url as cover_url
                  from t_dance_music t1
                  left join t_dance_works t2 on t1.music_id=t2.dance_music_id
                  group by t1.music_id
                  order by {0} desc
               """.format(order_tp)
        rows = self.base.exec_r(sql)

        for row in rows:
            music = self._convert_music_object(row)
            result.append(music)

        return result

    def get_dance_score(self, dance_id=0):
        score = 0
        sql = """
                select score from t_dance_work_grade
                where id=%s
        """
        rows = self.base.exec_r(sql, dance_id)
        if len(rows):
            score = rows[0]['score']

        return score

    def get_grade_detail(self, dance_id=0, work_id=0):
        dancer = self.get_dancer_by_dance_id(dance_id=dance_id, work_id=work_id)

        combo = {
            '-1': 5,
            '3' : 2,
            '4' : 2,
            '5' : 10
        }

        dancer.combo = combo

        return dancer.toDict()

    def get_dancers_by_music_id(self, music_id):
        result = []
        sql  = """
                  select t1.id,t1.user_id, t1.timestamp, t1.duration, t1.score,
                  t3.user_icon,t3.nickname
                  from t_dance_work_grade t1
                  join (select max(timestamp) mts ,user_id from t_dance_work_grade group by user_id) t2
                  on t2.user_id=t1.user_id and t2.mts=t1.timestamp
                  left join t_open_user_profile t3 on t1.user_id = t3.id
                  left join t_dance_works t4 on t4.id=t1.work_id
                  where t4.dance_music_id=%s
                  limit 5
               """
        rows = self.base.exec_r(sql, music_id)

        for row in rows:
            music = self._convert_dancer_object(row)
            result.append(music)

        return result

    def get_dancers_by_work_id(self, work_id='', tp=0):
        order_map = {
            0 : "timestamp",
            1 : "score"
        }
        order_tp = order_map[tp]
        result = []
        #sql  = """
        #          select t1.id,t1.user_id, t1.timestamp, t1.duration, t1.score,
        #          t2.nickname, t2.user_icon
        #          from t_dance_work_grade t1
        #          join (select max({0}) marg ,user_id from t_dance_work_grade group by user_id) temp
        #          on t1.{0}=temp.marg and t1.user_id=temp.user_id
        #          left join t_open_user_profile t2
        #          on t1.user_id = t2.id
        #          where t1.work_id=%s
        #          order by {0} desc
        #       """.format(order_tp)
        sql = """
                SELECT t1.id,t1.user_id, t1.timestamp, t1.duration, t1.score,t3.nickname, t3.user_icon,
                (SELECT count(DISTINCT score) FROM t_dance_work_grade t2 WHERE t1.score<t2.score and t2.work_id=%s)+1 AS rank
                FROM t_dance_work_grade t1
                left join t_open_user_profile t3 on t1.user_id = t3.id
                where t1.work_id=%s
                order by {0} desc
                limit 20
        """.format(order_tp)
        rows = self.base.exec_r(sql, work_id, work_id)

        for row in rows:
            dancer = self._convert_dancer_object(row)
            result.append(dancer)

        return result

    def get_dancer_by_dance_id(self, dance_id=0, work_id=0):
        #sql  = """
        #          select t1.id,t1.user_id, t1.timestamp, t1.duration, t1.score,
        #          t2.nickname, t2.user_icon
        #          from t_dance_work_grade t1
        #          left join t_open_user_profile t2
        #          on t1.user_id = t2.id
        #          where t1.id=%s and t1.work_id=%s
        #       """
        sql = """
                SELECT t1.id,t1.user_id, t1.timestamp, t1.duration, t1.score,t3.nickname, t3.user_icon,
                (SELECT count(DISTINCT score) FROM t_dance_work_grade AS t2 WHERE t1.score<t2.score and t2.work_id=%s)+1 AS rank
                FROM t_dance_work_grade AS t1 left join t_open_user_profile t3 on t1.user_id=t3.id
                WHERE t1.id = %s and t1.work_id=%s
                limit 20
        """
        rows = self.base.exec_r(sql, work_id, dance_id, work_id)
        dancer = _Dancer()

        if len(rows):
            dancer = self._convert_dancer_object(rows[0])
            return dancer


    def get_work_by_id(self, work_id=0):
        sql  = """
                  select t1.id, t1.user_id, t1.video_id, t1.player_num,
                  t2.name, t2.create_time, t2.pic_url, t2.duration, t2.play_count,
                  t3.nickname, t3.user_icon, t3.cover_id, t5.game_id, t6.music_type
                  from t_dance_works t1
                  left join t_medias t2 on t2.media_id=t1.video_id
                  left join t_open_user_profile t3 on t1.user_id = t3.id
                  left join t_video_game t5 on t5.video_id=t1.video_id
                  left join t_dance_music t6 on t6.id=t1.dance_music_id
                  where t1.id=%s
               """
        rows = self.base.exec_r(sql, work_id)

        work_obj = _Work()
        if len(rows):
            work_obj = self._convert_work_object(rows[0])

        return work_obj

    def get_work_by_dance_id(self, dance_id=0):
        sql  = """
                  select t1.id, t1.user_id, t1.video_id, t1.player_num,
                  t2.name, t2.create_time, t2.pic_url, t2.duration, t2.play_count,
                  t3.nickname, t3.user_icon, t3.cover_id, t5.game_id, t6.music_type
                  from t_dance_work_grade t4
                  left join t_dance_works t1 on t4.work_id=t1.id
                  left join t_medias t2 on t2.media_id=t1.video_id
                  left join t_open_user_profile t3 on t1.user_id = t3.id
                  left join t_video_game t5 on t5.video_id=t1.video_id
                  left join t_dance_music t6 on t6.id=t1.dance_music_id
                  where t4.id=%s
               """
        rows = self.base.exec_r(sql, dance_id)

        work_obj = _Work()
        if len(rows):
            work_obj = self._convert_work_object(rows[0])

        return work_obj




    def get_works_by_music_id(self, music_id='', tp=0):
        order_map = {
            0 : "play_count,create_time",
            1 : "play_count",
            2 : "create_time",
        }
        ordertype_map = {
            'play_count'  : 'desc',
            'create_time' : 'desc'
        }
        order_tp = order_map[tp]
        lst = []
        for item in order_tp.split(','):
            ot = ordertype_map.get(item)
            order_comp = '%s %s'%(item,ot)
            lst.append(order_comp)

        order_tp = ','.join(lst)

        result = []
        sql  = """
                  select count(1) as play_count, t1.id, t1.user_id, t1.video_id, t1.player_num,
                  t2.name, t2.create_time, t2.pic_url, t2.duration, t2.play_count,
                  t3.nickname, t3.user_icon, t3.cover_id, t5.game_id, t6.music_type
                  from t_dance_works t1
                  left join t_medias t2 on t2.media_id=t1.video_id
                  left join t_open_user_profile t3 on t1.user_id = t3.id
                  left join t_dance_work_grade t4 on t4.work_id=t1.id
                  left join t_video_game t5 on t5.video_id=t1.video_id
                  left join t_dance_music t6 on t6.id=t1.dance_music_id
                  where t1.dance_music_id=%s
                  group by t1.id
                  order by {0}
               """.format(order_tp)
        rows = self.base.exec_r(sql, music_id)

        for row in rows:
            music = self._convert_work_object(row)
            result.append(music)

        return result

    def get_work_data(self, work_id=0):
        sql = """
                select data from t_dance_works where id=%s
        """
        rows = self.base.exec_r(sql, work_id)

        data = ''

        if len(rows):
            data = rows[0]['data']

        return data


    def add_work_dancer(self, user_id=0, work_id=0, score=0, duration=0, ts=0):
        sql = """
            insert into t_dance_work_grade(work_id, user_id, timestamp, duration, score)
            values(%s,%s,%s,%s,%s)
        """
        return self.base.exec_w(sql, work_id, user_id, ts, duration, score)


    def _convert_music_object(self, row):
        danceMusic               = _DanceMusic()
        danceMusic.id            = row.get('id')
        danceMusic.music_id      = row.get('music_id')
        danceMusic.name          = row.get('name')
        danceMusic.player        = row.get('player')
        danceMusic.duration      = row.get('duration') or 0
        danceMusic.high_duration = row.get('high_duration') or 0
        danceMusic.url           = row.get('url') or ''
        danceMusic.create_time   = row.get('create_time') or 0
        danceMusic.cover_url     = row.get('cover_url') or ''
        danceMusic.music_type    = row.get('music_type') or 0
        #danceMusic.share_time    = row.get('share_time') or 0
        return danceMusic

    def _convert_dancer_object(self, row):
        dancer           = _Dancer()
        dancer.user_id   = row.get('user_id')
        dancer.nickname  = row.get('nickname')
        dancer.user_icon = row.get('user_icon')
        dancer.timestamp = row.get('timestamp')
        dancer.duration  = row.get('duration')
        dancer.score     = row.get('score')
        dancer.dance_id  = row.get('id')
        dancer.rank      = row.get('rank') or 0

        return dancer

    def _convert_work_object(self, row):
        work             = _Work()
        work.id          = row.get('id')
        work.user_id     = row.get('user_id')
        work.video_id    = row.get('video_id')
        work.nickname    = row.get('nickname')
        work.user_icon   = row.get('user_icon')
        work.name        = row.get('name')
        work.duration    = row.get('duration')
        work.create_time = row.get('create_time')
        work.pic_url     = row.get('pic_url')
        work.game_id     = row.get('game_id')
        work.play_count  = row.get('play_count')
        work.player_num  = row.get('player_num')
        work.music_type  = row.get('music_type') or 0

        cover_id         = row.get('cover_id')
        if not work.pic_url and cover_id:
            from dao.media import Media
            media        = Media(self.base)
            cover_url    = media.get_media_url(cover_id)
            work.pic_url = cover_url

        return work

class _DanceMusic(object):
    def __init__(self):
        self.id          = 0
        self.music_id    = 0
        self.name        = ''
        self.player      = ''
        self.duration    = 0
        self.high_duration = 0
        self.url         = ''
        self.cover_url   = ''
        self.create_time = 0
        #self.share_time  = 0
        self.dancers     = []
        self.music_type  = 0

    def toDict(self):
        dic = {}
        dic['id']          = self.id
        dic['music_id']    = self.music_id
        dic['name']        = self.name
        dic['author']      = self.player
        dic['duration']    = self.duration
        dic['start_time']  = self.high_duration
        dic['url']         = self.url
        dic['cover_url']   = self.cover_url
        dic['create_time'] = self.create_time
        dic['music_type']  = self.music_type
        #dic['share_time']  = self.share_time
        d_arr              = []
        for dancer in self.dancers:
            d_arr.append(dancer.toDict())
        dic['dancers']     = d_arr

        return dic

class _Dancer(object):
    def __init__(self):
        self.user_id   = 0
        self.nickname  = ''
        self.user_icon = ''
        self.timestamp = 0
        self.duration  = 0
        self.score     = 0
        self.dance_id  = 0
        self.rank      = 0
        self.combo     = {}

    def toDict(self):
        dic = {}
        dic['user_id']   = self.user_id
        dic['nickname']  = self.nickname
        dic['user_icon'] = self.user_icon
        dic['timestamp'] = self.timestamp
        dic['duration']  = self.duration
        dic['score']     = self.score
        dic['dance_id']  = self.dance_id
        dic['rank']      = self.rank
        dic['combo']     = self.combo

        return dic

class _Work(object):
    def __init__(self):
        self.id        = 0
        self.user_id   = 0
        self.video_id  = 0
        self.game_id   = 0
        self.nickname  = ''
        self.user_icon = ''
        self.name      = ''
        self.duration  = 0
        self.create_time = 0
        self.pic_url     = ''
        self.play_count  = 0
        self.player_num  = 1
        self.music_type  = 0

    def toDict(self):
        dic = {}
        dic['id']          = self.id
        dic['user_id']     = self.user_id
        dic['video_id']    = self.video_id
        dic['game_id']     = self.game_id
        dic['nickname']    = self.nickname
        dic['user_icon']   = self.user_icon
        dic['name']        = self.name
        dic['duration']    = self.duration
        dic['create_time'] = self.create_time
        dic['cover_url']   = self.pic_url
        dic['play_count']  = self.play_count
        dic['player_num']  = self.player_num
        dic['music_type']  = self.music_type

        return dic
