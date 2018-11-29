# -*- coding: UTF-8 -*-
import time

from lib.log import get_logger
from lib.config import read_db_config
from dao.base import BaseDao

logger = get_logger('db')

class UserProfile(object):
    def __init__(self, base=None):
        self.base = base or BaseDao(read_db_config())

    def close(self):
        if self.base:
            self.base.close()
            self.base = None

    def update_user_icon(self, usericon, userid):
        if usericon and userid:
            sql = """
                    update t_open_user_profile set user_icon=%s where id=%s
            """

            self.base.exec_w(sql, usericon, userid)

    def update_user_profile_diy(self, user_id=0, signature='', nickname='', user_icon='', user_pics=[]):
        import time
        ts = int(time.time())
        cover_id = ''
        if user_pics and len(user_pics):
            sql = """
                    insert ignore into t_medias (url,player,name,media_id,user_id,type)
                    values (%s,%s,%s,%s,%s,1)
            """
            for item in user_pics:
                url  = item['url']
                name = item['name']
                media_id = item['md5']
                if not (url and media_id):
                    continue
                self.base.exec_w(sql, url, nickname, name, media_id, user_id)
                if item['isCover']:
                    cover_id = media_id
        if cover_id:
            sql = """
                     update t_open_user_profile set nickname=%s,signature=%s,update_time=%s,user_icon=%s,cover_id=%s,isDiy=1
                     where id=%s
                """
            self.base.exec_w(sql, nickname, signature, ts, user_icon, cover_id, user_id)
        else:
            sql = """
                     update t_open_user_profile set nickname=%s,signature=%s,update_time=%s,user_icon=%s,isDiy=1
                     where id=%s
                """
            self.base.exec_w(sql, nickname, signature, ts, user_icon, user_id)


    def update_user_profile(self, obj=None, isDiy=0):
        sql = """
                update t_open_user_profile set nickname=%s, user_icon=%s, update_time=%s
                where uid=%s and update_time < %s and isDiy=%s
        """

        self.base.exec_w(sql, obj.nickname, obj.usericon, obj.share_time, obj.uid, obj.share_time, isDiy)

    def get_uid_by_userid(self, userid):
        sql = "select uid from t_open_user_profile where id=%s"
        rows = self.base.exec_r(sql, userid)
        if (len(rows) > 0):
            return rows[0]['uid']

    def get_user_profile(self, uid):
        sql  = "select id, nickname, user_icon, level, uid, signature, rank, rank_info from t_open_user_profile where id=%s"
        rows = self.base.exec_r(sql, uid)

        result = []
        if (len(rows) > 0):
            user_profile = self._convert_object(rows[0])
            result.append(user_profile)
        return result

    def get_user_profile_by_uid(self, uid):
        sql  = "select id, nickname, user_icon, level, uid, signature, rank, rank_info from t_open_user_profile where uid=%s"
        rows = self.base.exec_r(sql, uid)

        result = []
        if (len(rows) > 0):
            user_profile = self._convert_object(rows[0])
            result.append(user_profile)
        return result

    def get_user_profile_by_id(self, userid):
        sql  = "select id, nickname, user_icon, level, uid, signature, rank, rank_info from t_open_user_profile where id=%s"
        rows = self.base.exec_r(sql, userid)

        result = []
        if (len(rows) > 0):
            user_profile = self._convert_object(rows[0])
            result.append(user_profile)
        return result

    def get_user_profile_by_ids(self, userids):
        if not userids or not len(userids):
            return None

        chars = ','.join(['%s'] * len(userids))
        args  = []
        args.extend(userids)
        sql  = """
                select id, nickname, user_icon, level, uid, signature, rank, rank_info, update_time
                from t_open_user_profile where id in ({0})
            """.format(chars)
        rows = self.base.exec_r(sql, *args)

        data  = []
        for row in rows:
            user_profile = self._convert_object(row)
            data.append(user_profile)
        return data


    def get_followers_num(self, uid):
        sql = "select count(1) as num from t_open_user_follow_list where userid2=%s and status=1"
        rows = self.base.exec_r(sql, uid)
        num = 0
        if (len(rows) > 0):
            num = rows[0]['num']

        return num

    def get_following_num(self, uid):
        sql = "select count(1) as num from t_open_user_follow_list where userid1=%s and status=1"
        rows = self.base.exec_r(sql, uid)
        num = 0
        if (len(rows) > 0):
            num = rows[0]['num']

        return num


    def get_all_followings(self, user_id = 0):
        sql    = '''
                select t2.id, t2.nickname, t2.user_icon, t2.level, t2.uid
                from t_open_user_follow_list t1 left join t_open_user_profile t2 on t1.userid2=t2.id
                where t1.status=1 and t1.userid1=%s and t2.uid_type=2
                order by t1.update_time desc
            '''
        rows      = self.base.exec_r(sql, user_id)

        result = []
        for row in rows:
            user_profile = self._convert_object(row)
            result.append(user_profile)

        return result



    def get_master_list(self, page_size = 10, page_num = 0, app_list = None):
        # 按播放次数查找达人
        offset    = (page_num - 1) * page_size
        sql       = '''
                select SQL_CALC_FOUND_ROWS t2.id as id, t2.nickname as nickname, t2.user_icon as user_icon,
                       t2.level as level, t2.uid as uid, sum(t1.play_count) as total_play_count
                from t_videos t1 left join t_open_user_profile t2 on t1.uid=t2.uid
                where t2.uid is not null and t2.nickname!='' and t2.uid_type=2
                group by 1 order by 2 desc limit %s, %s
                '''
        total_sql = "select FOUND_ROWS() as total"
        rows      = self.base.exec_r(sql, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        # 达人记录总数
        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        # 生成达人列表
        result = []
        for row in rows:
            user_dic                = {}
            user_profile            = self._convert_object(row)
            user_dic['userid']      = user_profile.no
            user_dic['nickname']    = user_profile.nickname
            user_dic['icon']        = user_profile.user_icon
            user_dic['level']       = user_profile.level
            user_dic['items']       = self._get_master_app_list(user_profile.uid) # 达人应用列表
            user_dic['is_follow']   = self._is_follow(user_profile.uid) # 达人是否被关注过
            user_dic['follow_icon'] = "http://img.qq.com/icon" # 被关注的图标url
            user_dic['play_count']  = int(row['total_play_count']) #self._get_play_count(row.uid) # 达人播放次数

            result.append(user_dic)

        return (total, result)

    def _is_follow(self, userid):
        sql  = "select count(1) as total from t_open_user_follow_list where status=1 and uid=%s"
        rows = self.base.exec_r(sql, userid)
        
        if (len(rows) > 0 and rows[0]['total'] > 0):
            return True
        return False

    def _get_master_app_list(self, userid):
        sql = '''
                select distinct t1.content_id as id, t1.content_name as name, t1.icon_url as url
                from t_content t1 left join t_video_game t2 on t1.content_id=t2.game_id
                     left join t_videos t3 on t3.video_id=t2.video_id
                where t1.content_name not in ('LOL') and t1.status=1
                      and t3.uid=%s
            '''
        rows = self.base.exec_r(sql, userid)

        item_list = []
        for row in rows:
            dic = {}
            dic['app_name'] = row['name']
            dic['app_icon'] = row['url']
            item_list.append(dic)
        return item_list
    
    def _get_play_count(self, userid):
        sql  = "select sum(play_count) as total from t_videos where uid=%s"
        rows = self.base.exec_r(sql, userid)

        if (len(rows) > 0 and rows[0]['total'] > 0):
            return rows[0]['total']
        return 0

    def get_watch_by_user(self, user_id = 0, page_size = 10, page_num = 0):
        offset = (page_num - 1) * page_size
        sql    = '''
                select SQL_CALC_FOUND_ROWS t2.id, t2.nickname, t2.user_icon, t2.level, t2.uid
                from t_open_user_follow_list t1 left join t_open_user_profile t2 on t1.userid2=t2.id
                where t1.status=1 and t1.userid1=%s and t2.uid_type=2
                order by t1.update_time desc limit %s, %s
            '''
        total_sql = "select FOUND_ROWS() as total"
        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        result = []
        for row in rows:
            user_profile = self._convert_object(row)
            result.append(user_profile)

        return (total, result)

    def get_watch_by_user_all(self, user_id = 0):
        sql    = '''
                select SQL_CALC_FOUND_ROWS t2.id, t2.nickname, t2.user_icon, t2.level, t2.uid
                from t_open_user_follow_list t1 left join t_open_user_profile t2 on t1.userid2=t2.id
                where t1.status=1 and t1.userid1=%s and t2.uid_type=2
                order by t1.update_time desc
            '''
        total_sql = "select FOUND_ROWS() as total"
        rows      = self.base.exec_r(sql, user_id)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        result = []
        for row in rows:
            user_profile = self._convert_object(row)
            result.append(user_profile)

        return (total, result)


    def get_fans_by_user(self, user_id = 0, page_size = 10, page_num = 0):
        offset = (page_num - 1) * page_size
        sql    = '''
                select SQL_CALC_FOUND_ROWS t2.id, t2.nickname, t2.user_icon, t2.level, t2.uid
                from t_open_user_follow_list t1 left join t_open_user_profile t2 on t1.userid1=t2.id
                where t1.status=1 and t1.userid2=%s and t2.uid_type=2
                order by t1.update_time desc limit %s, %s
            '''
        total_sql = "select FOUND_ROWS() as total"
        rows      = self.base.exec_r(sql, user_id, offset, page_size)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        result = []
        for row in rows:
            user_profile = self._convert_object(row)
            result.append(user_profile)

        return (total, result)

    def watch(self, watch_id, watched_id, status):
        # 添加一条关注关系
        now = int(time.time())
        sql = '''
                replace into t_open_user_follow_list(userid1, userid2, update_time, status)
                values(%s, %s, %s, %s)
            '''
        self.base.exec_w(sql, watch_id, watched_id, now, status)

        # 往watched_id 发送关注系统消息
        self._add_message(watch_id, watched_id, status)

    # userid1是否关注了userid2
    def is_watch(self, userid1, userid2):
        sql  = 'select userid1, userid2 from t_open_user_follow_list where status=1 and userid1=%s and userid2=%s'
        rows = self.base.exec_r(sql, userid1, userid2)

        if (len(rows) > 0):
            return True
        else:
            return False

    def get_message_number(self, userid):
        sql  = 'select type,count(1) as number from t_message where status=0 and to_user=%s group by type'
        rows = self.base.exec_r(sql, userid)

        data = {'system': 0, 'watch': 0, 'praise': 0, 'cluster': 0}
        for row in rows:
            if (row['type'] == 1):
                data['system'] = row['number']
            elif (row['type'] == 2):
                data['watch'] = row['number']
            elif (row['type'] == 3):
                data['praise'] = row['number']
            elif (row['type'] == 4):
                data['cluster'] = row['number']
        return data

    def _add_message(self, watch_id, watched_id, status):
        watch_profile   = self.get_user_profile(watch_id)
        watched_profile = self.get_user_profile(watched_id)
        
        if (len(watch_profile) <= 0):
            return
        
        if (status == 1):
            title_txt = '{0}关注了你'.format(watch_profile[0].nickname)
            message   = title_txt
        else:
            title_txt = '{0}取消关注了你'.format(watch_profile[0].nickname)
            message   = title_txt
            
        msg_type    = 2
        from_user   = watch_id
        to_user     = watched_id
        submit_time = int(time.time())
        msg_status  = 0
        sql = '''
                insert into t_message(title, message, type, from_user, to_user, submit_time, status)
                values(%s, %s, %s, %s, %s, %s, %s)
            '''
        
        #logger.info('title => {0}, message => {1}, type => {2}, from => {3}, to => {4}, submit time => {5}, status => {6}'.format(title_txt, message, msg_type, from_user, to_user, submit_time, msg_status))
        self.base.exec_w(sql, title_txt, message, msg_type, from_user, to_user, submit_time, msg_status)

    def get_user_content(self, userid):
        sql = '''
                select t2.game_id,t3.content_name,t3.icon_url,sum(t1.play_count) as play_count
                from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id
                     left join t_content t3 on t3.content_id=t2.game_id
                     left join t_open_user_profile t4 on t4.uid=t1.uid
                where t4.id=%s
                group by 1,2
            '''
        rows = self.base.exec_r(sql, userid)

        play_count = 0
        result     = []
        for row in rows:
            dic_tmp         = {}
            dic_tmp['id']   = row['game_id']
            dic_tmp['icon'] = row['icon_url']
            play_count      = play_count + int(row['play_count'])
            result.append(dic_tmp)

        return (play_count, result)

    def _convert_object(self, row):
        user_profile             = _UserProfile()
        user_profile.no          = row['id']
        user_profile.nickname    = row['nickname']
        user_profile.user_icon   = row['user_icon']
        user_profile.level       = row['level']
        user_profile.uid         = row['uid']
        user_profile.signature   = row.get('signature') or ''
        user_profile.rank        = row.get('rank') or 0
        user_profile.rankInfo    = row.get('rank_info') or ''
        user_profile.update_time = row.get('update_time') or 0
        return user_profile

class _UserProfile(object):
    def __init__(self, no = 0, nickname = '', user_icon = '', level = 0, uid = ''):
        self.no        = no
        self.nickname  = nickname
        self.user_icon = user_icon
        self.level     = level
        self.uid       = uid
        self.signature = ''
        self.rank      = 0
        self.rankInfo  = ''
        self.update_time = 0

    def toDict(self):
        dic = {}
        dic['userid']    = self.no
        dic['nickname']  = self.nickname
        dic['icon']      = self.user_icon
        dic['level']     = self.level
        dic['signature'] = self.signature
        dic['isV']       = self.rank == 1
        dic['VInfo']     = self.rankInfo
        return dic

