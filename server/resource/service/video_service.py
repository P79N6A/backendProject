# -*- coding: UTF-8 -*-
import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.video import Video
from dao.media import Media
from lib.config import read_link_domain
from service.user_profile_service import ProfileService

logger = get_logger('busi')
Domain = read_link_domain()

class VideoService(object):
    def __init__(self, base=None):
        self.__base = base

    def add_video_good(self, vid):
        self.__base   = self.__base or BaseDao()
        video        = Video(self.__base)
        video.add_good_count(vid)

    def get_hot_video(self):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_hot_video(20)

        arr = []
        for row in rows:
            v = row.toDict()
            arr.append(v)

        data              = {}
        data['item_name'] = '最热视频'
        data['total']     = total
        data['items']     = arr
        return data

    def get_discover_video(self, page_num):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_discover_video(30, page_num)

        arr = []
        for row in rows:
            v = row.toDict()
            arr.append(v)

        data           = {}
        data['videos'] = arr
        data['total']  = total
        return data

    def get_watch_video(self, user_id, page_num):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_watch_video(user_id, page_num, 30)

        data            = {}
        data['masters'] = rows
        data['total']   = total
        return data

    def get_class_video(self, page_num, type_class = None, type_id = 'all', tag = 'all'):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_video_by_type(page_num, 30, type_id, type_class, tag)

        arr = []
        for row in rows:
            v = row.toDict()
            arr.append(v)

        data             = {}
        data['contents'] = arr
        data['total']    = total
        return data

    def get_video_by_user(self, user_id = 0, req_user_id = 0, begin_sec = 0, begin_usec=0, batch_num=30):
        data              = {}
        data['videos']    = []
        data['total']     = 0
        data['user_info'] = []
        data['is_watch']  = False

        self.__base   = self.__base or BaseDao()
        try:
            req_user_info = {'req_user_id':req_user_id, 'begin_sec':begin_sec, 'begin_usec':begin_usec }
            res_obj = self.get_video_by_users(user_id=user_id, req_user_ids=[req_user_info], batch_num=batch_num)

            data['videos']    = res_obj.get('videos')
            data['total']     = res_obj.get('total')
            data['user_info'] = res_obj.get('user_info')
            ps  = ProfileService(base = self.__base)
            is_watch   = ps.is_watch(user_id, req_user_id)
            data['is_watch'] = is_watch
        except:
            logger.error(traceback.format_exc())
        finally:
            return data


    def _convert_openid(self, openid_list):
        from lib.httptool import open_url_json
        send_data = {}
        lp_appid = 'wx9ce8f64a4c9b3308'
        send_data['target_appid'] = lp_appid
        send_data['openid_list']  = openid_list
        tmp = open_url_json(url='http://%s/weixin/openid/convert'%Domain, data=send_data)
        if not (tmp and isinstance(tmp, dict) and tmp.get("data")):
            logger.error('convert uid to lpuid error, uid:%s lp_appid:%s'%(uid,lp_appid))
            return None
        return tmp.get('data')
        #res = tmp.get('data')

    def _get_watch_users(self, user_id):
        from service.watch_service import WatchService
        ws = WatchService(base = self.__base)
        try:
            req_user_ids = []
            userids = ws.get_watch_all(user_id)
            for userid in userids:
                req_user_ids.append({'req_user_id':int(userid), 'begin_sec':0, 'begin_usec':0 })

            return req_user_ids
        except:
            logger.error('get watch error:%s'%traceback.format_exc())
            return None

    def _get_herotime_client(self):
	from l5.get_router import get_router
	from transport.client import UDPClient
	from lib.config import read_l5_info

        modid,cmdid = read_l5_info()
        host,port = get_router(modid, cmdid)
        if not (host and port):
           logger.error('l5 error')
           return None

        udp_client = UDPClient(host=host, port=port)
        return udp_client


    def get_video_by_users(self, user_id = 0, req_user_ids=[], batch_num=30):
        import time
        from adjuster.hero_adjuster import HeroAdjuster
        from dao.common import assemble_adjuster
        from dao.user_profile import UserProfile

        self.__base   = self.__base or BaseDao()
        if not req_user_ids:
            req_user_ids = _get_watch_users(user_id)
        if not req_user_ids:
            return None

        udp_client        = self._get_herotime_client()
        arr = []
        data              = {}
        data['videos']    = arr
        data['total']     = 0
        data['user_info'] = []

        try:
            video         = Video(self.__base)
            user          = UserProfile(self.__base)
            uid_tmps      = []
            userid_tmps   = []
            uid_time_map  = {}
            uid_user_id_map = {}
            user_id_uid_map = {}
            user_id_profile_map = {}
            for user_item in req_user_ids:
                #req_user_id is chuanchuan id
                #uid     is chuanchuan openid
                req_user_id  = user_item['req_user_id']
                if not req_user_id:
                    logger.warn('req_user_id is null, continue')
                    continue
                uid  = user.get_uid_by_userid(req_user_id)
                if not uid:
                    logger.error('uid is null, req_user_id:%s'%req_user_id)
                    continue
                    #return None

                uid_user_id_map[uid] = req_user_id
                user_id_uid_map[req_user_id] = uid
                uid_tmps.append(uid)
                userid_tmps.append(req_user_id)
                uid_time_map[uid] = (user_item.get('begin_sec') or 0,user_item.get('begin_usec') or 0)
            if not len(uid_tmps):
                logger.warn('uid_tmps is null, return None')
                return None


            res = self._convert_openid(uid_tmps)

            openids            = []
            openid_user_id_map = {}
            for uid_tmp in uid_tmps:
                lp_openid                     = res.get(uid_tmp)
                if not lp_openid:
                    logger.warn('convert uid:%s to lp uid fail, maybe it is qq openid'%uid)
                    continue
                userid                        = uid_user_id_map.get(uid_tmp)
                openid_user_id_map[lp_openid] = userid
                begin_sec, begin_usec         = uid_time_map.get(uid_tmp)
                openids.append({'uid':lp_openid.encode("utf-8"),'begin_sec':begin_sec, 'begin_usec':begin_usec })

            if not len(openids):
                logger.warn('lp openids is null, maybe it is all qq openid:%s'%uid_tmps)
                return None


            logger.info('convert openid success %s->%s, start get videos'%(uid_tmps,openids))

            adjuster = HeroAdjuster(udp_client)
            logger.info('[Time]:get_videos_by_batch_users,start:%s'%time.time())
            res_obj = adjuster.get_videos_by_batch_users(openids=openids,
                                                         batch_num=batch_num)
            logger.info('[Time]:get_videos_by_batch_users,end:%s'%time.time())

            obj_tmp = []
            for item in res_obj:
                datas = item.get('datas')
                req_userid = openid_user_id_map.get(item.get('uid'))
                for info in datas:
                    #logger.info('debug:info:%s'%info)
                    obj = assemble_adjuster(info)

                    row_id = video.add_video(video_obj=obj)
                    if row_id:
                        video.add_video_game(video_obj=obj)
                        user.update_user_profile(obj=obj)

                    obj.uid        = user_id_uid_map[req_userid]
                    obj.userid     = req_userid
                    obj_tmp.append(obj)
                    #logger.info('get_video_by_users, add video info:%s'%obj.toDict())
                end_sec    = item.get('end_sec') or 0
                end_usec   = item.get('end_usec') or 0
                #end_sec 0 represent has no more datas, so do not response to client.
                if not end_sec:
                    continue
                data['user_info'].append({'req_user_id':req_userid, 'begin_sec':end_sec, 'begin_usec':end_usec})

            for user_profile in user.get_user_profile_by_ids(userid_tmps):
                user_id_profile_map[user_profile.no] = user_profile

            for obj in obj_tmp:
                profile      = user_id_profile_map[obj.userid]
                obj.nickname = profile.nickname
                obj.usericon = profile.user_icon
                arr.append(obj.toDict())

            data['total']    = len(arr)
        except:
            logger.error(traceback.format_exc())
        finally:
            udp_client.close()
            return data


    def get_chuan_video_by_user(self, user_id = 0, req_user_id = 0, page_num = 0):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_chuan_video_by_user(page_num, 30, req_user_id)

        arr = []
        for row in rows:
            v = row.toDict()
            arr.append(v)

        data             = {}
        data['videos']   = arr
        data['total']    = len(arr)
        return data

    def get_share_video_info(self, video_id='', page_num=1):
        self.__base   = self.__base or BaseDao()
        data          = {}
        video         = Video(self.__base)
        vobj          = video.get_videoinfo_by_id(video_id)
        if not vobj:
            ##不存在，则把最热的视频放上去
            data['info']       = {}
            data['similars']   = []
            total, videos_obj = video.get_hot_video()
            for obj in videos_obj:
                data['similars'].append(obj.toDict())

            return data
        similars      = video.get_similar_video_list(video_id=video_id, page_num=page_num)
        data['info']  = vobj.toDict()
        data['similars'] = similars
        return data

    def get_user_see_history(self, user_id = 0, req_user_id = 0, page_num = 0):
        self.__base   = self.__base or BaseDao()
        video         = Video(self.__base)
        (total, rows) = video.get_user_see_history(page_num, 30, req_user_id)

        arr = []
        for row in rows:
            v = row.toDict()
            arr.append(v)

        service  = ProfileService()
        is_watch = service.is_watch(user_id, req_user_id)
        service.close()

        data             = {}
        data['videos']   = arr
        data['total']    = total
        data['is_watch'] = is_watch
        return data

    def _del_video_by_vid(self, vid=''):
        self.__base   = self.__base or BaseDao()
        if not vid:
            logger.error('_del_video_by_vid fail, need vid')
            return False
        try:
            video         = Video(self.__base)
            video.del_video_by_vid(vid)
        except:
            logger.error('_del_video_by_vid fail, %s'% traceback.format_exc())
            return False

        logger.info('_del_video_by_vid success,vid:%s'%vid)
        return True


    def get_url_by_vid(self, vid='', game_id=0):
        import time
        data = {'url':''}

        self.__base = self.__base or BaseDao()
        video       = Video(self.__base)
        game_id     = game_id or video.get_gameid_by_vid(vid)

        if not game_id:
            logger.warn('no game_id for vid:%s'%vid)
            return data
            #raise Exception('no game_id for vid:%s'%vid)

        local_games = [1000001]
        if int(game_id) in local_games:
            media = Media(self.__base)
            url = media.get_media_url(vid)
            if not url:
                logger.error('vid:%s game_id:%s url is null'%(vid, game_id))
            data['url'] = url
            return data

        tries = 3
        url = self._get_download_url(vid, game_id)
        while tries > 0 and (not url):
            tries -= 1
            time.sleep(1)
            logger.warning('url is null, try again.')
            url = self._get_download_url(vid, game_id)


        if not url:
            self._del_video_by_vid(vid)
            logger.error('get url failue, vid:%s,game_id:%s'% (vid,game_id))
            raise Exception('get url failue, vid:%s,game_id:%s'% (vid,game_id))

        data['url'] = url
        return data

    def _get_download_url(self, vid, game_id):
        if not (vid and game_id):
            logger.error('need game_id vid')
            return ''
        from lib.config import read_l5_info
        from transport.client import UDPClient
        from l5.get_router import get_router
        from adjuster.adjuster_tool import get_download_info_req

        udp_client = None
        try:
            modid,cmdid = read_l5_info()
            host,port = get_router(modid, cmdid)
            if not (host and port):
                logger.error('l5 get error')
                raise Exception('l5 get error')

            udp_client = UDPClient(host=host, port=port)

            resp = get_download_info_req(vid=vid.encode("utf-8"),game_id=int(game_id), udp_client=udp_client)
            if not resp:
                logger.warning('vid:%s download info is null.' % vid)
                return ''
            if len(resp.ul) and len(resp.cl):
                url = resp.ul[0]
                cl  = resp.cl[0]
                v_url = '%s%s?vkey=%s' % (url.url, resp.fn, cl.vkey)

                return v_url
        except:
            logger.error(traceback.format_exc())
        finally:
            if udp_client:
                udp_client.close()

        return ''


    def close(self):
        if (self.__base is not None):
            self.__base.close()

