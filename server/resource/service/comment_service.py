import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.base_comment import BaseComment
from dao.user_comment import VideoComment

logger = get_logger('busi')

class CommentService(object):
    def __init__(self):
        self.__base = None

    def get_base_comment(self, video_type = 'all'):
        self.__base = BaseDao()
        baseComment = BaseComment(self.__base)

        data   = []
        result = baseComment.get_comment()
        for value in result:
            data.append(value.toDict())
        return data

    def add_video_comment(self, vid, content, userid, comment_time, uname):
        self.__base  = BaseDao()
        videoComment = VideoComment(self.__base)
        videoComment.add_video_comment(vid, userid, comment_time, content, uname)

    def get_video_comment(self, vid):
        self.__base  = BaseDao()
        videoComment = VideoComment(self.__base)
        data         = videoComment.get_video_comment(vid)
        if (data):
            return self._convert_to_xml(data)
        else:
            return ''

    def close(self):
        if (self.__base is not None):
            self.__base.close()

    def _convert_to_xml(self, comments):
        xml ="<?xml version='1.0' encoding='UTF-8'?><i>{0}</i>"
        
        ds = []
        for comment in comments:
            ds.append(comment.toString())
        tmp_str = ''.join(ds)
        
        return xml.format(tmp_str)


