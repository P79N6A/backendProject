# -*- coding: UTF-8 -*-
import traceback
import sys
sys.path.append('/usr/local/app/nb')
import warnings
warnings.filterwarnings("ignore")

from hero.qt_herlper import QtHelper
import hero.proto.hero_time_recommend_pb2 as pb_hero_rec
import hero.proto.hero_time_pb2 as pb_hero
from lib.config import read_l5_info
from lib.log import get_logger
#from busi.dao.common import get_second_c_by_gameid
#from id_cvt import get_opedid_by_uid
from l5.get_router import get_router
from transport.client import UDPClient
from adjuster.adjuster_tool import *

fetcher = get_logger('main')
openid_logger = get_logger('main')
logger = get_logger('main')

class HeroAdjuster(object):
    def __init__(self, udp_client):
        self.udp_client = udp_client

    def build_multi_game_send_buf(self, game_ids=[],begin_sec=0,begin_usec=0, batch_num=10, v_type=0, uin=0, openid=''):
        #if not (game_ids and len(game_ids)):
        #    logger.error('build_multi_game_send_buf args error.')
        #    return None

        try:
            qt = QtHelper()
            sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                     pb_hero.SUBCMD_GET_VIDEOTIMELINE_MULTI,
                                     8031,uin)

            req = pb_hero.GetVideoTimelineMultiReq()
            req.type     = v_type
            #if game_ids and len(game_ids):
            #    req.game_id_list.extend(game_ids)
            req.need_tag = 1
            req.begin_sec  = begin_sec
            req.begin_usec = begin_usec
            req.num        = batch_num
            if openid:
                req.uuid   = 'LA-' + openid
                req.flag   = openid
            elif uin:
                req.user_uin = uin
                req.flag     = str(uin)
            else:
                fetcher.error('need uin or openid')
                return None

            res = qt.buildSendPkg(sess, req)
            buf = res.serialize()
            return buf

        except:
            fetcher.error('build_multi_game_send_buf get error:%s'%traceback.format_exc())

    def recv_multi_game_resp(self, client=None):
        if not client:
            logger.error('recv_multi_game_resp args error.')
            return None

        try:
            bb = client.recvData()

            qt = QtHelper()
            resp = qt.parseReceivePkg(bb)
            resp.unserialize()
            resp_str = str(buffer(resp.body_str)[:])
            pb_resp = pb_hero.GetVideoTimelineMultiRsp()
            pb_resp.ParseFromString(resp_str)

            return pb_resp
        except:
            fetcher.error('recv_multi_game_resp get error:%s'%traceback.format_exc())


    def get_videoInfo_by_user(self, uin=0, game_id=0, begin_sec=0, client=None,
                              begin_usec=0, batch_num=10, v_type=0, openid=None):
        try:
            qt = QtHelper()
            sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                     pb_hero.SUBCMD_GET_VIDEOTIMELINE,
                                     8031,uin)

            client = client or self.udp_client
 
            req = pb_hero.GetVideoTimelineReq()
            req.type     = v_type
            req.game_id  = game_id
            req.need_tag = 1
            req.begin_sec  = begin_sec
            req.begin_usec = begin_usec
            req.num      = batch_num
            if openid:
                req.uuid = 'LA-' + openid
            elif uin:
                req.user_uin = uin
            else:
                fetcher.error('need uin or openid')
                return None
    
            res = qt.buildSendPkg(sess, req)
    
            client.sendData(buf=res.serialize())
            bb = client.recvData()
    
            resp = qt.parseReceivePkg(bb)
            resp.unserialize()
            resp_str = str(buffer(resp.body_str)[:])
            pb_resp = pb_hero.GetVideoTimelineRsp()
            pb_resp.ParseFromString(resp_str)
     
            return pb_resp
        except:
            fetcher.error('get error:%s'%traceback.format_exc())


    def get_rec_req(self, game_id=0, area_id=0, type=1, num=10,
                    from_num=0, uin=0):
        try:
            qt = QtHelper()
            sess = qt.createSessInfo(pb_hero_rec.CMD_HEROTIMESVR, pb_hero_rec.SUBCMD_GET_RECOMMEND_VIDEO,
                                     8031, uin)
    
            req = pb_hero_rec.GetRecommendVideoReq()
            req.game_id = game_id
            req.area_id = area_id
            req.type = type
            req.num = num
            req.from_num = from_num
    
    
            res = qt.buildSendPkg(sess, req)
            #b = res.serialize()
    
            self.udp_client.sendData(buf=res.serialize())
            bb = self.udp_client.recvData()
    
            resp = qt.parseReceivePkg(bb)
            resp.unserialize()
            resp_str = str(buffer(resp.body_str)[:])
            pb_resp = pb_hero_rec.GetRecommendVideoRsp()
            pb_resp.ParseFromString(resp_str)
    
            return pb_resp
        except:
            fetcher.error('get error:%s'%traceback.format_exc())
    
    def get_videosInfo_req(self, vid_list=[], user_uin=0, area_id=0, game_id=0):
        try:
            qt = QtHelper()
            sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                     pb_hero.SUBCMD_GET_VIDEOSINFO,
                                     8031,user_uin)
            req = pb_hero.GetVideosInfoReq()
            req.user_uin = user_uin
            req.area_id  = area_id
            req.vid_list.extend(vid_list)
            req.game_id  = game_id
            req.need_tag = 1
    
            res = qt.buildSendPkg(sess, req)
            #b = res.serialize()
    
            self.udp_client.sendData(buf=res.serialize())
            bb = self.udp_client.recvData()
    
            resp = qt.parseReceivePkg(bb)
            resp.unserialize()
            resp_str = str(buffer(resp.body_str)[:])
            pb_resp = pb_hero.GetVideosInfoRsp()
            pb_resp.ParseFromString(resp_str)
     
            return pb_resp.result,pb_resp.video_info_list
        except:
            fetcher.error('get error:%s'%traceback.format_exc())
    

    #end QT


    def get_video_info_by_vid_list(self, vid_list=[], game_id=0, appid='wx9ce8f64a4c9b3308'):
        result,v_info_list = self.get_videosInfo_req(vid_list=vid_list,game_id=game_id)

        if result != 0:
            fetcher.error('get v_info req error')
            return -1

        obj_arr = []
        for info in v_info_list:
            v_obj = assemble_v_obj(info, game_id, appid)
            if not (v_obj['nickname'] and v_obj['user_icon']):
                fetcher.warn('[WARNING]nickname or user_icon is null,obj:%s'%v_obj)
            if not v_obj:
                continue
            obj_arr.append(v_obj)
        return obj_arr


    def adjust(self, batch=1, batch_num=10, from_num=0,game_id=0, appid='wx9ce8f64a4c9b3308'):
        obj_arr = []
        while batch > 0:
            fetcher.info('batch:%s start ...'%batch)
            resp = self.get_rec_req(game_id=game_id,from_num=from_num,num=batch_num)
            if resp.result != 0:
                fetcher.error('get rec req error')
                return -1
            vid_list = [item.vid for item in resp.video_list]
            tmp_arr = self.get_video_info_by_vid_list(vid_list=vid_list, game_id=game_id, appid=appid)
            if not (tmp_arr and len(tmp_arr)):
                fetcher.info('get_video_info_by_vid_list retur null, continue')
                continue

            weixin_arr, qq_arr = convert_uid(tmp_arr)
            obj_arr.extend(weixin_arr)
            obj_arr.extend(qq_arr)
            from_num += len(tmp_arr)
            batch -= 1
        return obj_arr


    def get_my_videos(self, batch_num=10, game_id=0, uin=0, v_type=0, appid='wx9ce8f64a4c9b3308',openid='', begin_sec=0, begin_usec=0, flag=True):

        obj_arr    = []
        begin_sec  = begin_sec or 0
        begin_usec = begin_usec or 0
        tmp_arr    = []
        fetcher.info('get_my_videos start, begin_sec:%s,begin_usec:%s,batch_num:%s,uin:%s'%(begin_sec,begin_usec,batch_num,uin))
        resp = self.get_videoInfo_by_user(game_id=game_id,begin_sec=begin_sec,begin_usec=begin_usec,batch_num=batch_num,uin=uin,v_type=v_type,openid=openid)
        if not resp:
            fetcher.error('get my videos error,  resp is null')
            return [],0,0
        if resp.result != 0:
            fetcher.error('get my videos error:%s'%resp)
            return [],0,0

        begin_sec  = resp.end_sec
        begin_usec = resp.end_usec

        fetcher.info('get:%s items of my videos' % resp.total_num)
        fetcher.info('get:%s items of my videos in fact' % len(resp.video_list))
        for info in resp.video_list:
            v_obj = assemble_v_obj(info, game_id, appid, flag=flag)
            if not v_obj:
                continue
            tmp_arr.append(v_obj)

        if len(tmp_arr):
            weixin_arr, qq_arr = convert_uid(tmp_arr)
            obj_arr.extend(weixin_arr)
            obj_arr.extend(qq_arr)

        return (obj_arr, begin_sec, begin_usec)


    def get_all_my_videos(self, batch_num=10, game_id=0, uin=0, v_type=0, appid='wx9ce8f64a4c9b3308',openid='', begin_sec=0, begin_usec=0, flag=True):

        obj_arr    = []
        begin_sec  = begin_sec or 0
        begin_usec = begin_usec or 0
        init       = 1
        tmp_arr    = []
        while(init or begin_sec):
            init = 0
            fetcher.info('get_all_my_videos start, begin_sec:%s,begin_usec:%s,batch_num:%s,uin:%s'%(begin_sec,begin_usec,batch_num,uin))
            resp = self.get_videoInfo_by_user(game_id=game_id,begin_sec=begin_sec,begin_usec=begin_usec,batch_num=batch_num,uin=uin,v_type=v_type,openid=openid)
            if not resp:
                fetcher.error('get my videos error,  resp is null')
                break
            if resp.result != 0:
                fetcher.error('get my videos error:%s'%resp)
                break
            fetcher.info('get:%s items of my videos' % resp.total_num)
            begin_sec  = resp.end_sec
            begin_usec = resp.end_usec
            fetcher.info('get:%s items of my videos in fact' % len(resp.video_list))
            for info in resp.video_list:
                v_obj = assemble_v_obj(info, game_id, appid, flag=flag)
                if not v_obj:
                    continue
                tmp_arr.append(v_obj)

        if len(tmp_arr):
            weixin_arr, qq_arr = convert_uid(tmp_arr)
            obj_arr.extend(weixin_arr)
            obj_arr.extend(qq_arr)


        return obj_arr


    def get_videos_by_batch_users(self, batch_num=5, game_ids=None, appid='wx9ce8f64a4c9b3308', uin=0, openids=[], uins=[], ip='', port=0):
        #if not game_ids:
        #    game_ids = [2103041,1007058,1007039,1007044,1007042,1007053,1007060]
        if not (ip and port):
            modid,cmdid = read_l5_info()
            ip,port = get_router(modid, cmdid)

        if not (ip and port):
            logger.error('ip or port is null')
            return []

        udp_client = UDPClient(host=ip, port=port)
        end_sec    = 0
        end_usec   = 0
        obj_arr = []

        try:
            for item in openids:
                uid        = item.get('uid') or ''
                if not uid:
                    continue
                begin_sec  = item.get('begin_sec') or 0
                begin_usec = item.get('begin_usec') or 0

                fetcher.info('get_videos_by_batch_users start, begin_sec:%s,begin_usec:%s,batch_num:%s,openid:%s'%(begin_sec,begin_usec,batch_num,uid))
                buf = self.build_multi_game_send_buf(game_ids=game_ids,
                                                       begin_sec=begin_sec,begin_usec=begin_usec,batch_num=batch_num,
                                                       uin=uin,v_type=0,openid=uid)
                udp_client.sendData(buf=buf)

            for item in uins:
                uid        = item.get('uid') or ''
                if not uid:
                    continue
                begin_sec  = item.get('begin_sec') or 0
                begin_usec = item.get('begin_usec') or 0

                fetcher.info('get_videos_by_batch_users start, begin_sec:%s,begin_usec:%s,batch_num:%s,uin:%s'%(begin_sec,begin_usec,batch_num,uid))
                buf = self.build_multi_game_send_buf(game_ids=game_ids,
                                                       begin_sec=begin_sec,begin_usec=begin_usec,batch_num=batch_num,
                                                       uin=uid,v_type=0)
                udp_client.sendData(buf=buf)

            loops = len(openids) + len(uins)
            while loops > 0:
                uid_datas = {'uid':'','end_sec':0, 'end_usec':0, 'datas':[]}
                loops -= 1
                resp = self.recv_multi_game_resp(udp_client)

                if not resp:
                    fetcher.error('get_videos_by_batch_users error, resp is null')
                    continue
                if resp.result != 0:
                    fetcher.error('get_videos_by_batch_users error, resp.resp is not 0:%s'%resp)
                    continue
                fetcher.info('get:%s %sitems of get_videos_by_batch_users in fact' % (resp.flag,len(resp.video_list)))
                end_sec  = resp.end_sec
                end_usec = resp.end_usec
                flag     = resp.flag

                for info in resp.video_list:
                    v_obj = assemble_v_obj(info, None, appid, flag=False)
                    if not v_obj:
                        continue
                    uid_datas['datas'].append(v_obj)
                uid_datas['end_sec']  = end_sec
                uid_datas['end_usec'] = end_usec
                uid_datas['uid']      = flag
                obj_arr.append(uid_datas)

        except:
            logger.error(traceback.format_exc())
        finally:
            udp_client.close()
            return obj_arr


def test_multi(ip,port):
    openids = [{'uid':'o6zB8wT0AIXgl6EFGS2sxzFsWyFg', 'begin_sec':0, 'begin_usec':0 }]
    uins = [{'uid':461807758}]
    game_ids = [1007039,1007058]
    modid,cmdid = read_l5_info()
    h,p = get_router(modid, cmdid)
    if not (h and p):
        print 'l5 get error'
        return
    #udp_client = UDPClient(host=h, port=p)

    hero_adjuster = HeroAdjuster(None)
    arr = hero_adjuster.get_videos_by_batch_users(openids=openids,game_ids=game_ids,ip=ip,port=port)
    #arr, t1, t2 = hero_adjuster.get_videos_by_batch_users(uins=uins,game_ids=game_ids,ip=ip,port=port)
    print arr

def test_my_video():
    from busi.dao.base import BaseDao
    from busi.dao.data import Video

    import time

    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',
                                                    t),'%Y-%m-%d %H:%M:%S'))
    #ts = long(time1)
    ts = 1519660800

    modid,cmdid = read_l5_info()
    host,port = get_router(modid, cmdid)
    if not (host and port):
        print 'l5 get error'
        sys.exit(1)
    udp_client = UDPClient(host=host, port=port)
    hero_adjuster = HeroAdjuster(udp_client)
    #resp = get_openid_by_uuid(uuid='LA-o6zB8wQxpM_kk0ns29fqsMh4s3lo')
    #print resp
    b = BaseDao()
    video_dao = Video(b)
    try:
        #obj_arr = hero_adjuster.adjust(game_id=1007039)
        obj_arr, t1, t2 = hero_adjuster.get_my_videos(game_id=1007058,uin=289296918, batch_num=50)
        #obj_arr, t1, t2 = hero_adjuster.get_my_videos(game_id=1007058,openid='o6zB8wT0AIXgl6EFGS2sxzFsWyFg')
        for obj in obj_arr:
            print obj
            #if obj['share_time'] >= ts:
            #    video_dao.add_item(obj)
            #    video_dao.add_video_game(obj['vid'], 1007039)
        print t1, t2
    except:
        print traceback.format_exc()
    finally:
        udp_client.close()


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8') 

    try:
        test_my_video()
        #test_multi(ip='10.157.68.38',port=32100)
    except:
        print traceback.format_exc()

