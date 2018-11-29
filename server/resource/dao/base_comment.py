from lib.log import get_logger

class BaseComment(object):
    def __init__(self, base):
        self.base   = base
        self.logger = get_logger('db')

    def get_comment(self, video_type = 'all'):
        sql = "select id,video_type,content from t_base_comment where video_type=%s"

        result = []
        for val in self.base.exec_r(sql, video_type):
            comment            = _Comment()
            comment.f_id       = val['id']
            comment.video_type = val['video_type']
            comment.content    = val['content']
            result.append(comment)
        return result

class _Comment(object):
    def __init__(self, f_id = 0, video_type = '', content = ''):
        self.f_id       = f_id
        self.video_type = video_type
        self.content    = content

    def toDict(self):
        dic = {}
        dic['comment_id']   = self.f_id
        dic['comment_type'] = self.video_type
        dic['content']      = self.content
        return dic

