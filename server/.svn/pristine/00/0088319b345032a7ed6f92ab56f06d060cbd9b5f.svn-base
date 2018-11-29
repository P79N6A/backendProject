# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
#from dao.music import Music
from dao.dance import Dance
from commonlib.utils.tool import make_qrcode_image

logger = get_logger('busi')
domain = 'xinqiaoh5.sparta.html5.qq.com'

class QRCodeService(object):
    def __init__(self, base=None):
        self.__base = base or BaseDao()

    #def get_share_video_image(self, user_id=0, video_id=''):
    #    url   = 'http://%s/h5/share/video?userid=%s&video_id=%s'%(domain, user_id, video_id)
    #    image = make_qrcode_image(url, border=0)
    #    return image

    def get_profile_info_image(self, user_id=0):
        url   = 'http://%s/edit.html?userid=%s'%(domain, user_id)
        image = make_qrcode_image(url, border=0)
        return image

    def get_dance_grade_image(self, dance_id=0):
        url   = 'http://%s/dance.html?dance_id=%s'%(domain, dance_id)
        image = make_qrcode_image(url, border=0)
        return image

    def get_video_image(self, video_id=''):
        url   = 'http://%s/game.html?video_id=%s'%(domain, video_id)
        image = make_qrcode_image(url, border=0)
        return image


    def close(self):
        if (self.__base is not None):
            self.__base.close()
            self.__base = None
