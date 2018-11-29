# -*- coding: UTF-8 -*-
import MySQLdb
import sys
import datetime
import traceback

from lib.log import get_logger

tags = set();
categorys = set();

logger = get_logger('main')
class Video(object):

    def __init__(self,base):
        self.base = base

    def add_video_game(self,vid,game_id):
        try:
            sql = "replace into t_video_game(video_id,game_id) values (%s,%s)"
            self.base.exec_w(sql, vid, game_id)
        except:
            print "add_video_game videos:%s game_id:%s error:"%(vid, game_id), sys.exc_info()[0]
            raise

    def del_video(self, vid):
        try:
            sql = "delete from t_videos where video_id='%s'" % vid
            self.base.exec_w(sql)
            return True
        except:
            print "dele videos:%s error:"%vid, sys.exc_info()[0]
            return False

    def valid_video(self, data):
        if data and data.has_key('v_url') and data.has_key('pic_url') and\
        data.has_key('vid') and data.has_key('title') and\
        data.has_key('play_num') and data.has_key('good_num') and\
        data.has_key('duration') and data.has_key('share_time') and\
        data.has_key('definition') and data.has_key('uid'):
            return 1
        else:
            return 0

    def add_videos(self,data):
        time = datetime.datetime.now().strftime('%Y%m%d')
        try:
            if self.valid_video(data):
                sql = "replace into t_videos" +\
                "(video_id,name,res_url,pic_url,duration,create_time,src_type,play_count,good_count,share_time,definition,uid,appid) values" +\
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.base.exec_w(sql,data['vid'], data['title'],
                                 data['v_url'],data['pic_url'],
                                 data['duration'], time,
                                 1,data['play_num'],data['good_num'],data['share_time'],data['definition'],data['uid'],data.get('appid'))
                return 1
            return 0
        except:
            print "addVideos error:", sys.exc_info()[0]
            print traceback.format_exc()
            return 0

    def add_open_user_profile(self,data):
        try:
            sql = "select update_time from t_open_user_profile where uid=%s"
            uid = data.get('uid')
            vals = self.base.exec_r(sql,uid)
            if len(vals) > 0:
                val = vals[0]
                update_time = val.get('update_time') or 0
                share_time  = data.get('share_time') or 0
                if (int(share_time) > int(update_time)):
                    sql = "update t_open_user_profile set nickname=%s,user_icon=%s,update_time=%s where uid=%s"
                    args = (data.get('nickname'),data.get('user_icon'),data.get('share_time'),data.get('uid'))
                    logger.info('share_time:%s > update_time:%s, update:%s'%(share_time, update_time, sql%(args)))
                    self.base.exec_w(sql, *args)
                else:
                    logger.info('share_time:%s < update_time:%s, do not update.uid:%s'%(share_time, update_time, uid))
            else:
                args = (data.get('uid'), data.get('nickname'),data.get('user_icon'),data.get('share_time'),data.get('uid_type'))
                sql = "insert into t_open_user_profile(uid,nickname,user_icon,update_time,uid_type) values (%s,%s,%s,%s,%s)"
                self.base.exec_w(sql, *args)
                logger.info('insert new user:%s'%(sql%args))

            return 1
        except:
            print "add open user profile error:", sys.exc_info()[0]
            print traceback.format_exc()
            return 0

    def add_chuan_to_app(self,data):
        try:
            sql = "insert ignore into t_chuan_to_app(uid,appid,app_uid,update_time) values (%s,%s,%s,%s)"
            self.base.exec_w(sql,data.get('uid'), data.get('appid'),data.get('src_uid'),data.get('share_time'))

            return 1
        except:
            print "add open user profile error:", sys.exc_info()[0]
            print traceback.format_exc()
            return 0

    def add_categorys(self,data):
        try:
            if data['category'] not in categorys:
                if data['category']:
                    categorys.add(data['category'])
                    sql = "insert ignore into t_categorys (name) values (%s)"
                    self.base.exec_w(sql,data['category'])
        except:
            print "add categorys error:", sys.exc_info()[0]
            raise
        finally:
            pass
    
    def add_tags(self,data):
        try:
            for tag in data['tags']:
                if tag and tag not in tags:
                    sql = "insert ignore into t_tags (name) values (%s)"
                    tags.add(tag)
                    self.base.exec_w(sql,tag)
        except:
            print "add tags error:", sys.exc_info()[0]
            raise
        finally:
            pass
    
    def add_video_categorys(self,data):
        try:
            if data:
                sql = "replace into t_video_categorys (video_id,category) values (%s,%s)"
                self.base.exec_w(sql, data['vid'], data['category'])
        except:
            print "addVideosCategorys error:", sys.exc_info()[0]
            raise
        finally:
            pass
    
    def add_video_second_categorys(self,data):
        try:
            if data:
                sql = "replace into t_video_categorys (video_id,category,layer) values (%s,%s,%s)"
                self.base.exec_w(sql,data['vid'], data['second_c'], 1)
        except:
            print "addVideosSecondCategorys error:", sys.exc_info()[0]
            raise
        finally:
            pass
    
    def add_categorys_map(self,data):
        try:
            if data:
                sql = "insert ignore into t_category_childrens (f_f_category,f_c_category,layer) values (%s,%s,%s)"
                self.base.exec_w(sql, data['category'], data['second_c'], 0)
        except:
            print "addCategoryMap error:", sys.exc_info()[0]
            raise
        finally:
            pass
    
    def add_video_tags(self,data):
        try:
            for tag in data['tags']:
                if tag:
                    weight = 100
                    sql = "insert ignore into t_video_tags (video_id,tag,weight) values (%s,%s,%s)"
                    self.base.exec_w(sql, data['vid'], tag, weight)
        except:
            print "addVideoTags error:", sys.exc_info()[0]
            raise
        finally:
            pass
    def get_extern_vids(self, game_id=0):
        try:
            sql = "select t1.video_id from t_videos t1 left join t_video_game t2 on t1.video_id=t2.video_id where t1.src_type in (1,2) and t2.game_id=%s"
            vals = self.base.exec_r(sql, game_id)
            for val in vals:
                yield val['video_id']
        except:
            print "get_extern_vids error:", sys.exc_info()[0]

    def update_vid_url(self, vid, url):
        try:
            sql = "update t_videos set res_url=%s where video_id=%s"
            self.base.exec_w(sql, url, vid)
            return 1
        except:
            print "update_vid_url error:", sys.exc_info()[0]
            return 0 

    def get_zero_definition(self):
        try:
            sql = "select t1.video_id,t2.game_id from t_videos t1 join t_video_game t2 on t1.video_id = t2.video_id where t1.src_type in (1,2) and t1.definition=0"
            vals = self.base.exec_r(sql)
            for val in vals:
                vid = val['video_id']
                game_id = val['game_id']
                yield (vid, int(game_id))
        except:
            print traceback.format_exc()

    def get_zero_url(self):
        try:
            sql = "select t1.video_id,t2.game_id from t_videos t1 join t_video_game t2 on t1.video_id = t2.video_id where t1.src_type in (1,2) and t1.res_url=''"
            vals = self.base.exec_r(sql)
            for val in vals:
                vid = val['video_id']
                game_id = val['game_id']
                yield (vid, int(game_id))
        except:
            print traceback.format_exc()


    #def get_old_uid(self):
    #    try:
    #        sql = "select uid from t_videos where length(uid)=28"
    #        vals = self.base.exec_r(sql)
    #        for val in vals:
    #            uid = val['uid']
    #            yield uid
    #    except:
    #        print traceback.format_exc()


    def update_definition(self, vid, definition):
        try:
            sql = "update t_videos set definition=%s where video_id=%s"
            self.base.exec_w(sql, definition, vid)
            return 1
        except:
            print traceback.format_exc()
            return 0

    def update_url(self, vid, url):
        try:
            sql = "update t_videos set res_url=%s where video_id=%s"
            self.base.exec_w(sql, url, vid)
            return 1
        except:
            print traceback.format_exc()
            return 0


    def get_content_by_game_id(self, game_id):
        try:
            sql = "select content_name from t_content where content_id=%s"
            vals = self.base.exec_r_one(sql, game_id)
            return vals[0]['content_name'] if vals else None
        except:
            print traceback.format_exc()

    def add_item(self, item):
        if self.add_videos(item):
            if self.add_open_user_profile(item):
                self.add_chuan_to_app(item)
            #self.add_categorys(item)
            self.add_tags(item)
            #self.add_video_categorys(item)
            self.add_video_tags(item)
            #self.add_video_second_categorys(item)
            #self.add_categorys_map(item)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
