# -*- coding: UTF-8 -*-
import traceback
import sys
sys.path.append('/usr/local/app/nb')

from hero.qt_herlper import QtHelper
import hero.proto.hero_time_recommend_pb2 as pb_hero_rec
import hero.proto.hero_time_pb2 as pb_hero
from busi.dao.base import BaseDao
from busi.dao.data import Video
from adjuster.hero_adjuster import HeroAdjuster
from lib.log import get_logger
from l5.get_router import get_router
from lib.config import read_l5_info
from transport.client import UDPClient
from common.tool import get_video_meta_info

logger = get_logger('main')

class Updater(object):
    def __init__(self, video_dao, udp_client):
        self.udp_client = udp_client
        self.video_dao  = video_dao

    def get_download_url(self, vid, game_id):
        return self._get_download_url(vid, game_id)

    def _get_download_url(self, vid, game_id):
        from adjuster.adjuster_tool import get_download_info_req
        resp = get_download_info_req(vid=vid.encode("utf-8"),game_id=game_id, udp_client=self.udp_client)
        if not resp:
            print 'vid:%s download info is null.' % vid
            return ''
        if len(resp.ul) and len(resp.cl):
            url = resp.ul[0]
            cl  = resp.cl[0]
            v_url = '%s%s?vkey=%s' % (url.url, resp.fn, cl.vkey)

            return v_url

        return ''

    def update_url(self, game_id=0):
        for vid in self.video_dao.get_extern_vids(game_id):
            v_url = self._get_download_url(vid,game_id)
            logger.info('update vid:%s url:%s' % (vid,v_url))
            if v_url:
                if self.video_dao.update_vid_url(vid, v_url):
                    logger.info('update %s url success' % vid)
                else:
                    logger.info('update %s url error' % vid)
            else:
                logger.info('update %s url fail:url is null,delete it.' % vid)
                if self.video_dao.del_video(vid):
                    logger.info('delete %s success.'%vid)
                else:
                    logger.info('delete %s fail.'%vid)

    def fix_definition(self):
        for vid,game_id in self.video_dao.get_zero_definition():
            if not (vid and game_id):
                continue
            v_url = self._get_download_url(vid,game_id)
            if v_url:
                v_meta_info = get_video_meta_info(v_url)
                if v_meta_info and v_meta_info.has_key('height'):
                    definition = v_meta_info['height']
                    if definition:
                        self.video_dao.update_definition(vid, definition)
                    else:
                        logger.warn('[WARNING]vid:%s definition is null'%vid)
            else:
                logger.warn('[WARNING]vid:%s,game_id:%s download url is null'%(vid,game_id))

        #for vid,game_id in self.video_dao.get_zero_url():
        #    if not (vid and game_id):
        #        continue
        #    v_url = self._get_download_url(vid,game_id)
        #    if v_url:
        #        self.video_dao.update_url(vid, v_url)
        #    else:
        #        logger.warn('[WARNING]vid:%s,game_id:%s download url is null'%(vid,game_id))


    #def fix_uid(self):
    #    for o_uid in self.video_dao.get_old_uid():
    #        if not o_uid:
    #            continue
    #        n_uid = get_opedid_by_comid(o_uid)
    #        if not n_uid:
    #            logger.warn('[WARNING]get null new uid, old:%s'%n_uid)
    #            continue
    #        self.video_dao.update_videos_uid(o_uid, n_uid)
    #        self.video_dao.update_uid(o_uid, n_uid)


if __name__ == "__main__":
    modid,cmdid = read_l5_info()
    host,port = get_router(modid, cmdid)
    print host,port
    if not (host and port):
        print 'l5 get error'
	sys.exit(1)

    udp_client = UDPClient(host, port)
    vid = '61bbeb58abdf4813bb230837ae7df521'
    game_id = 1007058
    from adjuster.adjuster_tool import get_download_url_and_definition
    print get_download_url_and_definition(vid=vid,game_id=game_id,udp_client=udp_client)
    #updater.update_url(game_id)
