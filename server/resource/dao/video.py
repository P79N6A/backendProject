# -*- coding: UTF-8 -*-
import random

from lib.log import get_logger
from dao.common import get_video_obj
from dao.common import get_hot_video_obj

logger = get_logger('db')

class Video(object):
    def __init__(self, base):
        self.base = base

    def get_video_info(self, video_id):
        sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,"\
        "t1.duration,t1.play_count,t1.good_count,t1.version,t1.share_time,t1.uid,t1.appid,t2.category,t3.music_ids,"\
        "t4.nickname,t4.user_icon,t4.id as userid,t5.game_id "\
        "from t_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id "\
        "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
        "left join t_open_user_profile t4 on t4.uid=t1.uid "\
        "left join t_video_game t5 on t5.video_id=t1.video_id "\
        "where t1.video_id=%s"
        vals = self.base.exec_r(sql, vid)
        if vals:
            val = vals[0]
            v = get_video_obj(val)
            return v


    def get_gameid_by_vid(self, vid):
        sql = "select game_id from t_video_game where video_id=%s"
        vals = self.base.exec_r(sql, vid)
        if vals:
            val = vals[0]
            return val['game_id']
        else:
            return None

    def get_content_by_game_id(self, game_id):
        try:
            sql = "select content_name from t_content where content_id=%s"
            vals = self.base.exec_r_one(sql, game_id)
            return vals['content_name'] if vals else None
        except:
            print traceback.format_exc()


    def get_second_c_by_vid(self, vid=''):
        name = ''
        try:
            game_id = self.get_gameid_by_vid(vid)
            if game_id:
                name = self.get_content_by_game_id(game_id)
        except:
            logger.error(traceback.format_exc())

        return name

    def get_nickname_by_vid(self, uid=0):
        name = ''
        if not uid:
            return name
        try:
            sql = "select nickname from t_open_user_profile where id=%s"
            vals = self.base.exec_r(sql, uid)
            if len(vals):
                val = vals[0]
                name = val['nickname']

        except:
            logger.error(traceback.format_exc())

        return name

    def get_videoinfo_by_id(self, vid):
        sql = """
                select t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.video_id,
                    t1.play_count, t1.share_time, t1.name, t1.res_url, t1.src_type,
                    t2.id as userid, t2.nickname, t2.user_icon,t3.game_id
                from t_videos t1
                left join t_open_user_profile t2 on t2.uid=t1.uid
                left join t_video_game t3 on t3.video_id=t1.video_id
                where t1.video_id=%s
        """
        rows      = self.base.exec_r(sql, vid)
        if len(rows):
            v     = get_hot_video_obj(rows[0])
            return v


    def get_info_by_vid(self, vid):
        sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,"\
        "t1.duration,t1.play_count,t1.good_count,t1.version,t1.share_time,t1.uid,t1.appid,t2.category,t3.music_ids,"\
        "t4.nickname,t4.user_icon,t4.id as userid,t5.game_id "\
        "from t_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id "\
        "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
        "left join t_open_user_profile t4 on t4.uid=t1.uid "\
        "left join t_video_game t5 on t5.video_id=t1.video_id "\
        "where t1.video_id=%s"
        vals = self.base.exec_r(sql, vid)
        if vals:
            val = vals[0]
            v = get_video_obj(val)
            return v

    def get_top_video(self, top):
        sql = "select t1.pic_url,t1.res_url,t1.create_time,t1.src_type,t1.f_id,t1.video_id,t1.name,t1.definition,"\
        "t1.duration,t1.play_count,t1.good_count,t1.version,t1.share_time,t1.uid,t1.appid,t2.category,t3.music_ids,"\
        "t4.nickname,t4.user_icon,t4.id as userid "\
        "from t_videos t1 left join t_video_categorys t2 on t1.video_id=t2.video_id "\
        "left join t_music_recommend t3 on t1.video_id=t3.video_id "\
        "left join t_open_user_profile t4 on t4.uid=t1.uid "\
        "where t2.layer=1 and t1.definition>=1080 and t2.category not in (%s) order by t1.play_count desc limit %s"
        vals = self.base.exec_r(sql, 'LOL', top)
        for val in vals:
            v = get_video_obj(val)
            yield v

    def get_hot_video(self, top = 10):
#        sql = '''
#                select t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.video_id,
#                       t1.play_count, t1.share_time, t1.name, t1.res_url, t4.icon_url,
#                       t5.id, t5.nickname, t5.user_icon
#                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
#                     left join t_content t4 on t4.content_id=t3.game_id
#                     left join t_open_user_profile t5 on t5.uid=t1.uid
#                where t1.definition>=1080
#                order by t1.play_count desc limit %s
#        '''

        sql = '''
                select t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                where t5.uid_type=2
                order by t1.definition desc, t1.play_count desc limit %s
        '''


        rows  = self.base.exec_r(sql, top)
        data  = []
        total = 0
        for row in rows:
            total = total + 1
            v     = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def get_discover_video(self, page_size = 10, page_num = 0):
        offset    = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t1.src_type, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                where t5.uid_type=2
                order by t1.play_count desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def get_similar_video_list(self, video_id='', page_num=0, page_size=10):
        offset    = (page_num - 1) * page_size
        sql       = """
                select t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.video_id,
                    t1.play_count, t1.share_time, t1.name, t1.res_url, t1.src_type,
                    t3.id as userid, t3.nickname, t3.user_icon,t4.game_id
                from t_videos t1 join t_video_game t2 on t1.video_id = t2.video_id
                left join t_open_user_profile t3 on t3.uid=t1.uid
                left join t_video_game t4 on t4.video_id=t1.video_id
                where t2.game_id in (select game_id from t_video_game where video_id=%s)
                order by t1.play_count desc limit %s, %s
        """

        rows      = self.base.exec_r(sql, video_id, offset, page_size)
        data      = []
        for row in rows:
            v     = get_hot_video_obj(row)
            data.append(v.toDict())

        return data

    def get_watch_video(self, user_id, page_num = 0, page_size = 10):
        offset    = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon, t5.level, t1.share_time - mod(t1.share_time+8*3600, 86400) as order_time
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                     left join t_open_user_follow_list t6 on t6.userid2=t5.id
                where t6.status=1 and t6.userid1=%s and t5.uid_type=2
                order by order_time desc, t1.good_count desc, t1.uid asc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data          = []
        cur_user_data = {}
        cur_uid       = None
        pre_uid       = None
        for row in rows:
            pre_uid = cur_uid
            cur_uid = int(row['id'])
            v       = self.get_hot_video_obj(row)

            if ((pre_uid is not None ) and (cur_uid == pre_uid)):
                if (len(cur_user_data['videos']) > 4):
                    cur_user_data['is_more'] = True
                else:
                    cur_user_data['videos'].append(v)
            else:
                pre_uid               = cur_uid
                user_data             = {}
                videos                = []
                user_data['userid']   = int(row['id'])
                user_data['nickname'] = row['nickname']
                user_data['icon']     = row['user_icon']
                user_data['level']    = row['level']
                user_data['is_more']  = False
                user_data['videos']   = videos
                cur_user_data         = user_data
                user_data['videos'].append(v)
                data.append(user_data)

        return (total, data)

    def get_video_by_type(self, page_num = 0, page_size = 10, type_id = 'all', type_class = None, tag = 'all'):
        total = 0
        data  = []
        if (type_id != 'all' and tag != 'all'):
            (total, data) = self._get_video_by_type_tag(page_num, page_size, type_id, tag)
        elif (type_id != 'all' and tag == 'all'):
            (total, data) = self._get_video_by_type(page_num, page_size, type_id)
        elif (type_id == 'all' and tag != 'all'):
            (total, data) = self._get_video_by_tag(page_num, page_size, tag)
        else:
            (total, data) = self._get_video(page_num, page_size)

        return (total, data)

    def _get_video_by_type_tag(self, page_num = 0, page_size = 10, type_id = None, tag = None):
        offset = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t2.game_id, t3.icon_url,
                       t4.id as userid, t4.nickname, t4.user_icon
                from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id
                     left join t_content t3 on t3.content_id=t2.game_id
                     left join t_open_user_profile t4 on t4.uid=t1.uid
                     left join t_video_tags t5 on t5.video_id=t1.video_id
                where t2.game_id=%s and t5.tag=%s and t4.uid_type=2
                order by t1.share_time desc, t1.play_count desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, type_id, tag, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def _get_video_by_type(self, page_num = 0, page_size = 10, type_id = None):
        offset = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t2.game_id, t3.icon_url,
                       t4.id as userid, t4.nickname, t4.user_icon
                from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id
                     left join t_content t3 on t3.content_id=t2.game_id
                     left join t_open_user_profile t4 on t4.uid=t1.uid
                where t2.game_id=%s and t4.uid_type=2
                order by t1.share_time desc, t1.play_count desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, type_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def _get_video_by_tag(self, page_num = 0, page_size = 10, tag = None):
        offset = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t2.game_id, t3.icon_url,
                       t4.id as userid, t4.nickname, t4.user_icon
                from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id
                     left join t_content t3 on t3.content_id=t2.game_id
                     left join t_open_user_profile t4 on t4.uid=t1.uid
                     left join t_video_tags t5 on t5.video_id=t1.video_id
                where t5.tag=%s and t4.uid_type=2
                order by t1.share_time desc, t1.play_count desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, tag, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def _get_video(self, page_num = 0, page_size = 10):
        offset = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t2.game_id, t3.icon_url,
                       t4.id as userid, t4.nickname, t4.user_icon
                from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id
                     left join t_content t3 on t3.content_id=t2.game_id
                     left join t_open_user_profile t4 on t4.uid=t1.uid
                where t4.uid_type=2
                order by t1.share_time desc, t1.play_count desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def get_video_by_user(self, page_num = 0, page_size = 10, user_id = 0):
        offset    = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                where t1.src_type=1 and t5.id=%s
                order by t1.share_time desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def get_video_by_users(self, page_num = 0, page_size = 10, user_ids = []):
        total = 0
        data  = []
        if not (user_ids and len(user_ids) and page_num and page_size):
            return (total, data)
        chars = ','.join(['%s'] * len(user_ids))
        args = []
        args.extend(user_ids)
        offset    = (page_num - 1) * page_size
        args.append(offset)
        args.append(page_size)
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                where t1.src_type=1 and t5.id in ({0})
                order by t1.share_time desc limit %s, %s
        '''.format(chars)
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, *args)
        total_row = self.base.exec_r(total_sql)

        if (len(total_row) > 0):
            total = total_row[0]['total']

        for row in rows:
            v = get_video_obj(row)
            data.append(v)
        return (total, data)


    def get_chuan_video_by_user(self, page_num = 0, page_size = 10, user_id = 0):
        offset    = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t1.pic_url, t1.create_time, t1.definition, t1.duration, t1.src_type, t1.video_id,
                       t1.play_count, t1.share_time, t1.name, t1.res_url, t3.game_id, t4.icon_url,
                       t5.id as userid, t5.nickname, t5.user_icon
                from t_videos t1 left join t_video_game t3 on t1.video_id=t3.video_id
                     left join t_content t4 on t4.content_id=t3.game_id
                     left join t_open_user_profile t5 on t5.uid=t1.uid
                where t1.src_type=2 and t5.id=%s
                order by t1.share_time desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def get_user_see_history(self, page_num = 0, page_size = 10, user_id = 0):
        offset    = (page_num - 1) * page_size
        sql = '''
                select SQL_CALC_FOUND_ROWS t2.pic_url, t2.create_time, t2.definition, t2.duration, t2.src_type, t2.video_id,
                       t2.play_count, t2.share_time, t2.name, t2.res_url, t5.icon_url,
                       t3.id as userid, t3.nickname, t3.user_icon, t4.game_id
                from t_user_videos t1 left join t_videos t2 on t1.video_id=t2.video_id
                     left join t_open_user_profile t3 on t3.uid=t2.uid
                     left join t_video_game t4 on t4.video_id=t1.video_id
                     left join t_content t5 on t5.content_id=t4.game_id
                where t1.user_id=%s
                order by t2.share_time desc limit %s, %s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        data  = []
        for row in rows:
            v = get_hot_video_obj(row)
            data.append(v)
        return (total, data)

    def add_play_count(self, vid):
        sql = 'update t_videos set play_count=play_count+1 where video_id=%s'
        self.base.exec_w(sql, vid)

    def add_good_count(self, vid):
        sql = 'update t_videos set good_count=good_count+1 where video_id=%s'
        self.base.exec_w(sql, vid)

    def add_video(self, video_obj=None, src_type=1):
        import datetime
        time = datetime.datetime.now().strftime('%Y%m%d')
        if not video_obj:
            return 0
        sql = """
                insert ignore into t_videos (video_id,name,pic_url,
                duration,create_time,src_type,play_count,good_count,share_time,definition,uid,appid)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        row_id = self.base.exec_w(sql, video_obj.video_id, video_obj.name, video_obj.cover, video_obj.duration,
                        video_obj.create_time,src_type,video_obj.play_count,video_obj.good_count,
                        video_obj.share_time,video_obj.definition,video_obj.uid,video_obj.appid)
        #logger.info('debug:%s'%(sql%(video_obj.video_id, video_obj.name, video_obj.cover, video_obj.duration,
        #                video_obj.create_time,src_type,video_obj.play_count,video_obj.good_count,
        #                video_obj.share_time,video_obj.definition,video_obj.uid,video_obj.appid)))

        return row_id

    def add_video_game(self, video_obj=None):
        sql = """
                insert ignore into t_video_game(video_id, game_id) values(%s,%s)
        """

        self.base.exec_w(sql, video_obj.video_id, video_obj.game_id)


    def del_video_by_vid(self, vid):
        sql = 'delete from t_videos where video_id=%s'
        self.base.exec_w(sql, vid)

    #def _get_vidoe(self, val):
    #    v = {}

    #    v['cover']       = val['pic_url'] if val.has_key('pic_url') else ''
    #    v['create_time'] = val['create_time'] if val.has_key('create_time') else '0'
    #    v['definition']  = val['definition'] if val.has_key('definition') else 0
    #    v['duration']    = val['duration'] if val.has_key('duration') else 0
    #    v['video_id']    = val['video_id'] if val.has_key('video_id') else ''
    #    v['play_count']  = val['play_count'] if val.has_key('play_count') and val['play_count'] != 0 else random.randint(1, 10)
    #    v['share_time']  = val['share_time'] if val.has_key('share_time') else 0
    #    v['name']        = val['name'] if val.has_key('name') else ''
    #    v['url']         = val['res_url'] if val.has_key('res_url') else ''
    #    v['game_icon']   = val['icon_url'] if val.has_key('icon_url') else ''
    #    v['isMix']       = val['src_type'] == 2 if val.has_key('icon_url') else False

    #    if v['definition'] >= 1080:
    #        v['isHD'] = True
    #    else:
    #        v['isHD'] = False

    #    return v
