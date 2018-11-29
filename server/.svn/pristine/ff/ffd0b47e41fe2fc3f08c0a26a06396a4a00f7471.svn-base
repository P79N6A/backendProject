# -*- coding: UTF-8 -*-
import MySQLdb
import sys
import datetime
import traceback

tags = set();
categorys = set();

class VideoInfo(object):

    def __init__(self):
        self.duration = 0
        self.tags     = []
        self.url      = ''
        self.title    = ''
        self.video_id = ''
        self.category = '串烧'
        self.second_c = ''
        self.definition = 0
        self.game_id  = 0


class Video(object):

    def __init__(self,base):
        self.base = base

    def get_videoInfo_by_vids(self, vids=[]):
        if vids and len(vids):
            data = []
            try:
		args = []
		args.extend(vids)
                chars_vids = ','.join(['%s'] * len(vids)) if vids else "''"
                sql = "select t1.video_id,t1.name,t1.res_url,t1.duration,t1.definition,t3.game_id,t4.content_name,t5.user_icon,t5.nickname "\
                      "from t_videos t1 "\
                      "left join t_video_game t3 on t1.video_id=t3.video_id "\
                      "join t_content t4 on t4.content_id=t3.game_id " \
                      "join t_open_user_profile t5 on t5.uid=t1.uid "\
                      "where t1.video_id in ({0}) and t4.status=1".format(chars_vids)

                vals = self.base.exec_r(sql, *args)
                for val in vals:
                    obj = VideoInfo()
                    obj.duration   = val['duration']
                    obj.definition = val['definition']
                    obj.url = val['res_url']
                    obj.title = val['name']
                    obj.video_id = val['video_id']
                    obj.duration = val['duration']
                    obj.second_c = val['content_name']
                    obj.user_icon = val['user_icon']
                    obj.nickname  = val['nickname']
                    obj.game_id   = val['game_id']
                    sql = "select tag from t_video_tags where video_id=%s"
                    tags = self.base.exec_r(sql, obj.video_id)
                    for item in tags:
                        obj.tags.append(item['tag'])

                    data.append(obj)
                    #yield obj
                return data
            except GeneratorExit:
                pass
            except:
                print "get_videoInfo_by_vids vids:%s error:"%(vids), sys.exc_info()[0]
                print traceback.format_exc()
        else:
            print 'vids is null'

    def get_video_info_by_tags(self, game_id='', tags=None, video_num=10, withouts=[]):
        try:
            if tags and len(tags) and video_num and isinstance(video_num, int):
		args = []
		args.extend(tags)
		args.append(game_id)
                without_vids = [item.video_id for item in withouts if isinstance(item, VideoInfo)] if withouts and isinstance(withouts, list) else []
		args.extend(without_vids)
		args.append(video_num)
                chars_tags = ','.join(['%s'] * len(tags)) if tags else "''"
                chars_without = ','.join(['%s'] * len(without_vids)) if without_vids else "''"
                sql = "select sum(t2.weight) as sum_weight,t1.video_id,t1.name,t1.res_url,t1.duration,t1.duration,t4.content_name,t5.user_icon,t5.nickname "\
                      "from t_videos t1 "\
                      "left join t_video_tags t2 on t1.video_id=t2.video_id "\
                      "left join t_video_game t3 on t1.video_id=t3.video_id "\
                      "join t_content t4 on t4.content_id=t3.game_id " \
                      "join t_open_user_profile t5 on t5.uid=t1.uid "\
                      "where t2.tag in ({0}) and t3.game_id=%s and t1.video_id not in ({1}) and t4.status=1 and t1.src_type!=2 "\
                      "group by t1.video_id order by sum_weight,rand() limit %s".format(chars_tags, chars_without)

                vals = self.base.exec_r(sql, *args)
                for val in vals:
                    obj = VideoInfo()
                    obj.duration = val['duration']
                    obj.url = val['res_url']
                    obj.title = val['name']
                    obj.video_id = val['video_id']
                    obj.duration = val['duration']
                    obj.second_c = val['content_name']
                    obj.user_icon = val['user_icon']
                    obj.nickname = val['nickname']
                    sql = "select tag from t_video_tags where video_id=%s"
                    tags = self.base.exec_r(sql, obj.video_id)
                    for item in tags:
                        obj.tags.append(item['tag'])

                    yield obj
        except GeneratorExit:
            pass
        except:
            print "get_video_info_by_roles roles:%s, game_id:%s error:"%(tags, game_id), sys.exc_info()[0]
            print traceback.format_exc()


    def get_video_info_by_roles(self, game_id='', roles=None, video_num=10):
        return self.get_video_info_by_tags(game_id=game_id,tags=roles,video_num=video_num)

    def get_video_info_by_multi_kill(self, game_id='', multis=None, video_num=10):
        return self.get_video_info_by_tags(game_id=game_id,tags=multis,video_num=video_num)


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
                                 2,data['play_num'],data['good_num'],data['share_time'],data['definition'],data['uid'],data.get('appid'))
                return 1
            return 0
        except:
            print "addVideos error:", sys.exc_info()[0]
            print traceback.format_exc()
            return 0

    def add_open_user_profile(self,data):
        try:
            sql = "select max(update_time) as update_time from t_open_user_profile where uid=%s"
            val = self.base.exec_r_one(sql, data.get('uid'))
            if val:
                update_time = val['update_time'] or 0
                if data.get('share_time') and int(data.get('share_time')) > int(update_time):
                    sql = "update t_open_user_profile set nickname=%s,user_icon=%s,update_time=%s where uid=%s"
                    self.base.exec_w(sql, data.get('nickname'),data.get('user_icon'),data.get('share_time'),data.get('uid'))
            else:
                sql = "insert into t_open_user_profile(uid,nickname,user_icon,update_time) values (%s,%s,%s,%s)"
                self.base.exec_w(sql,data.get('uid'), data.get('nickname'),data.get('user_icon'),data.get('share_time'))

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


    def get_content_by_game_id(self, game_id):
        try:
            sql = "select content_name from t_content where content_id=%s"
            vals = self.base.exec_r_one(sql, game_id)
            return vals['content_name'] if vals else None
        except:
            print traceback.format_exc()


    def add_item(self, item):
        res = self.add_videos(item)
        if res:
            #self.add_open_user_profile(item)
            self.add_categorys(item)
            self.add_tags(item)
            self.add_video_categorys(item)
            self.add_video_tags(item)
            self.add_video_second_categorys(item)
            self.add_categorys_map(item)

class Chuan(object):
    def __init__(self,base):
        self.base = base

    def createJob(self, uid=0, vids=[]):
        import time
        try:
            if vids and len(vids):
                ts = long(time.time())
                sql = "insert into t_chuan_jobs(userid,create_time,status) values (%s,%s,%s)"
                insert_id = self.base.exec_w(sql, uid, ts, 0)

                chars_vids = ','.join(['(%s,%s)'] * len(vids)) if vids else None
                sql = "insert into t_chuan_job_detail(job_id, video_id) values {0}"
                sql = sql.format(chars_vids)
                args = []
                for vid in vids:
                    args.append(insert_id)
                    args.append(vid)
                self.base.exec_w(sql, *args)
                return insert_id
        except:
            print traceback.format_exc()
            return -1

    def update_chuan_status(self, jid=0, status=0, vid=''):
        import time
        try:
            ts = long(time.time())
            sql = "update t_chuan_jobs set status=%s, finish_time=%s, video_id=%s where id=%s"
            self.base.exec_w(sql, status, ts, vid, jid)
        except:
            print traceback.format_exc()

    def query_chuan_status(self, jid=0):
        try:
            status = -1
            vid = ''
            sql = "select status,video_id from t_chuan_jobs where id=%s"
            vals = self.base.exec_r(sql, jid)
            if vals and len(vals):
                status = vals[0]['status']
                vid = vals[0]['video_id']
            else:
                print 'no jid:%s found.'% jid
 
            return status,vid
        except:
            print traceback.format_exc()
            return status,vid

    def query_chuan_doing_jobs(self, uid=0):
        try:
            sql = "select id from t_chuan_jobs where userid=%s and status=0"
            vals = self.base.exec_r(sql, uid)
            for val in vals:
                yield int(val['id'])
 
        except:
            print traceback.format_exc()

    def get_userinfo_by_uid(self, uid=0):
        try:
            sql = "select nickname,uid from t_open_user_profile where id=%s"
            vals = self.base.exec_r(sql, uid)
            if len(vals):
                val = vals[0]
                nickname = val['nickname']
                uid      = val['uid']
                return nickname,uid

        except:
            print traceback.format_exc()
            return None

        return None

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
