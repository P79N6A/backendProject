# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.user_profile import UserProfile
from service.application_service import ApplicationService

logger = get_logger('busi')

class ProfileService(object):
    def __init__(self, base=None):
        self.__base = base

    #def get_chuan_id_by_openid(self, openid=''):
    #    self.__base = BaseDao()
    #    sql = "select id from t_open_user_profile where openid=%s"
    #    self.__base.exec_w(sql, openid)

    def get_uid_by_userid(self, userid):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        uid         = op.get_uid_by_userid(userid)

        return uid

    def add_invalid_icon(self, userid):
        from commonlib.service.session_service import SessionService
        from service.video_service import VideoService
        sessionS = SessionService(self.__base)
        isExit = sessionS.get_session(pool='invalid_icon', k=userid)
        if not isExit:
            #一个小时内不会重复请求
            sessionS.add_session(pool='invalid_icon', k=userid, v='.', expire=60*60)
            #sessionS.add_session(pool='invalid_icon', k=userid, v='.', expire=6)
            videoS = VideoService(self.__base)
            datas  = videoS.get_video_by_user(user_id=userid,req_user_id=userid,batch_num=1)
            videos = datas['videos']
            if videos and len(videos):
                video_obj = videos[0]
                user_icon = video_obj['usericon']
                if user_icon:
                    logger.info('get new user_icon:%s, now update db'%user_icon)
                    self.__base = self.__base or BaseDao()
                    op          = UserProfile(self.__base)
                    op.update_user_icon(user_icon, userid)
        else:
            logger.info('userid:%s has already in cache, do not update now'%userid)
            #get icon and update

    def insert_user_profile(self, obj):
        self.__base = self.__base or BaseDao()
        import time
        ts = int(time.time())
        uid_type = obj.get('uid_type') or 1
        sql = """
                 insert ignore into t_open_user_profile (uid,nickname,user_icon,sex,update_time,uid_type)
                 values(%s,%s,%s,%s,%s,%s)
            """

        #sql = """
        #         insert into t_open_user_profile (uid,nickname,user_icon,sex,update_time,uid_type)
        #         values(%s,%s,%s,%s,%s,%s)
        #         ON DUPLICATE KEY UPDATE nickname=%s,user_icon=%s,sex=%s,update_time=%s,id=LAST_INSERT_ID(id)
        #    """

        sex = 1 if obj['sex']=='男' else 0
        #sid = self.__base.exec_w(sql, obj['openid'], obj['nickname'], obj['usericon'], sex, ts, uid_type, obj['nickname'], obj['usericon'], sex, ts)
        sid = self.__base.exec_w(sql, obj['openid'], obj['nickname'], obj['usericon'], sex, ts, uid_type)
        return sid

    def update_user_profile(self, obj):
        self.__base = self.__base or BaseDao()
        import time
        ts = int(time.time())
        sql = """
                 update t_open_user_profile set nickname=%s,user_icon=%s,sex=%s,update_time=%s
                 where uid=%s and isDiy=0
            """
        sex = 1 if obj['sex']=='男' else 0
        self.__base.exec_w(sql, obj['nickname'], obj['usericon'], sex, ts, obj['openid'])

    def update_user_profile_diy(self, user_id=0, signature='', nickname='', user_icon='', user_pics=[]):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        op.update_user_profile_diy(user_id=user_id, signature=signature,
                                   nickname=nickname, user_icon=user_icon, user_pics=user_pics)


    def get_user_profile(self, uid):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        rows        = op.get_user_profile(uid)

        dic = {}        
        if (len(rows) > 0):
            dic = rows[0].toDict()
            dic['followers_num'] = op.get_followers_num(uid) or 0
            dic['following_num'] = op.get_following_num(uid) or 0
        
        data = {}
        data['profile'] = dic
        data['message'] = op.get_message_number(uid)
        return data

    def get_user_profile_by_uid(self, uid):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        rows        = op.get_user_profile_by_uid(uid)

        if (len(rows) > 0):
            return rows[0].toDict()

    def get_user_profile_by_id(self, userid):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        rows        = op.get_user_profile_by_id(userid)

        if (len(rows) > 0):
            return rows[0].toDict()

    def get_master_list(self, page_num):
        # 获取应用列表
        #service  = ApplicationService()
        #app_list = service.get_all_app()
        #service.close()

        self.__base = self.__base or BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_master_list(5, page_num)
      
        data = {}
        data['masters'] = rows
        data['total']   = total
        data['name']    = '猜你喜欢'
        return data

    def get_watch(self, user_id = 0, page_num = 0, page_size = 10):
        self.__base = self.__base or BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_watch_by_user(user_id, 30, page_num)

        is_big_v = False
        result   = []
        for row in rows:
            u = row.toDict()
            
            u['is_big_v'] = is_big_v
            if (is_big_v):
                is_big_v = False
            else:
                is_big_v = True
            
            (play_count, icons)   = op.get_user_content(u['userid'])
            u['total_play_count'] = play_count
            u['games']            = icons
            
            result.append(u)
        
        data             = {}
        data['watchs']   = result
        data['total']    = total
        return data

    def get_fans(self, user_id = 0, page_num = 0, page_size = 10):
        self.__base = self.__base or BaseDao()
        op            = UserProfile(self.__base)
        (total, rows) = op.get_fans_by_user(user_id, page_size, page_num)

        is_big_v = False
        result   = []
        for row in rows:
            u = row.toDict()
            
            u['is_big_v'] = is_big_v
            if (is_big_v):
                is_big_v = False
            else:
                is_big_v = True
            
            (play_count, icons)   = op.get_user_content(u['userid'])
            u['total_play_count'] = play_count
            u['games']            = icons
            
            result.append(u)
        
        data           = {}
        data['fans']   = result
        data['total']  = total
        return data

    def watch(self, watch_id, watched_id, status):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        op.watch(watch_id, watched_id, status)

        data              = {}
        data['op_result'] = '成功'
        return data

    def is_watch(self, userid1, userid2):
        self.__base = self.__base or BaseDao()
        op          = UserProfile(self.__base)
        return op.is_watch(userid1, userid2)

    def user_watch_relation(self, userid1, userid2):
        data = {}
        data['is_watch'] = self.is_watch(userid1, userid2)
        return data
        
    def close(self):
        if (self.__base is not None):
            self.__base.close()
            self.__base = None

