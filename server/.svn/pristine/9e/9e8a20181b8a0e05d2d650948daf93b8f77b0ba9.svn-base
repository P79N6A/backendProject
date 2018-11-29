from lib.log import get_logger

class VideoComment(object):
    def __init__(self, base):
        self.base   = base
        self.logger = get_logger('db')

    def get_video_comment(self, vid):
        sql = "select id,video_id,content,from_userid,from_name,comment_time,create_time from t_video_comment where video_id=%s"

        result = []
        for val in self.base.exec_r(sql, vid):
            comment              = _VideoComment()
            comment.f_id         = val['id']
            comment.video_id     = val['video_id']
            comment.content      = val['content']
            comment.from_userid  = val['from_userid']
            comment.from_name    = val['from_name']
            comment.comment_time = val['comment_time']
            comment.create_time  = val['create_time']
            result.append(comment)
        return result

    def add_video_comment(self, video_id, from_userid, comment_time, content, from_name):
        if not video_id or not from_userid or not comment_time or not content:
            self.logger.warn('need user_id,user id,comment time,comment content')
            return
        
        sql = "insert into t_video_comment(video_id,content,from_userid,from_name,comment_time,create_time) values (%s,%s,%s,%s,%s,now())"
        self.base.exec_w(sql, video_id, content, from_userid, from_name, comment_time)

class _VideoComment(object):
    def __init__(self, f_id = 0, video_id = 0, content = '', from_userid = 0,
            from_name = '', comment_time = 0, create_time = '1970-01-01 00:00:00'):
        self.f_id         = f_id
        self.video_id     = video_id
        self.content      = content
        self.from_userid  = from_userid
        self.from_name    = from_name
        self.comment_time = comment_time
        self.create_time  = create_time

    def toString(self):
        tmp_str = "<d p='{0},1,30,16777215,0,0,{1},{2}'>{3}</d>".format(self.comment_time/1000,
                self.from_userid, self.f_id, self.content)
        return tmp_str

