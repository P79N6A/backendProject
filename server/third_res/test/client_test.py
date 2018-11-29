# -*- coding: UTF-8 -*-
import traceback
import sys
#sys.path.append('/usr/local/app/third_res')

from udp_server_demo.client import UDPClient
from hero.qt_herlper import QtHelper
from l5.get_router import get_router
import hero.proto.hero_time_recommend_pb2 as pb_hero_rec
import hero.proto.hero_time_pb2 as pb_hero

TYPE_MAP = {
    1007039 : '王者荣耀',
    2 : '超神杀戮'
}

host,port = get_router(64176833, 131072)
if not host:
    print 'l5 get error'
    sys.exit(1)

def get_rec_req(udp_client, game_id=1007039, area_id=0, type=1, num=10,
                from_num=0):
    try:
        qt = QtHelper()
        sess = qt.createSessInfo(pb_hero_rec.CMD_HEROTIMESVR, pb_hero_rec.SUBCMD_GET_RECOMMEND_VIDEO,
                                 8031)

        req = pb_hero_rec.GetRecommendVideoReq()
        req.game_id = game_id
        req.area_id = area_id
        req.type = type
        req.num = num
        req.from_num = from_num


        res = qt.buildSendPkg(sess, req)
        #b = res.serialize()

        udp_client.sendData(host=host, port=port, buf=res.serialize())
        bb = udp_client.recvData()

        resp = qt.parseReceivePkg(bb)
        resp.unserialize()
        resp_str = str(buffer(resp.body_str)[:])
        pb_resp = pb_hero_rec.GetRecommendVideoRsp()
        pb_resp.ParseFromString(resp_str)

        return pb_resp
    except:
        print traceback.format_exc()

def get_videosInfo_req(udp_client, video_list, user_uin=0, area_id=0, game_id=1007039):
    try:
        qt = QtHelper()
        sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                 pb_hero.SUBCMD_GET_VIDEOSINFO,
                                 8031)
        vid_list = []
        for v_info in video_list:
            vid_list.append(v_info.vid)

        req = pb_hero.GetVideosInfoReq()
        req.user_uin = user_uin
        req.area_id  = area_id
        req.vid_list.extend(vid_list)
        req.game_id  = game_id


        res = qt.buildSendPkg(sess, req)
        #b = res.serialize()

        udp_client.sendData(host=host, port=port, buf=res.serialize())
        bb = udp_client.recvData()

        resp = qt.parseReceivePkg(bb)
        resp.unserialize()
        resp_str = str(buffer(resp.body_str)[:])
        pb_resp = pb_hero.GetVideosInfoRsp()
        pb_resp.ParseFromString(resp_str)
 
        return pb_resp.result,pb_resp.video_info_list
    except:
        print traceback.format_exc()

def get_download_info_req(udp_client=None, vid=0, platform=10, game_id=1007039):
    try:
        qt = QtHelper()
        sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                 pb_hero.SUBCMD_APPLY_DOWNLOAD_VIDEO,
                                 8031)

        req = pb_hero.ApplyDownloadVideoReq()
        req.file_uuid = vid
        req.platform  = platform
        req.game_id   = game_id


        res = qt.buildSendPkg(sess, req)
        #b = res.serialize()

        udp_client.sendData(host=host, port=port, buf=res.serialize())
        bb = udp_client.recvData()

        resp = qt.parseReceivePkg(bb)
        resp.unserialize()
        resp_str = str(buffer(resp.body_str)[:])
        pb_resp = pb_hero.ApplyDownloadVideoRsp()
        pb_resp.ParseFromString(resp_str)

        return pb_resp
    except:
        print traceback.format_exc()

def adjust_hero_v_info(udp_client=None, game_id=1007039):
    batch = 5
    batch_num = 10
    from_num  = 0
    obj_arr   = []
    obj_map   = {}
    while batch > 0:
	print 'from num:%s' % from_num
        resp = get_rec_req(udp_client=udp_client, game_id=game_id,from_num=from_num,num=batch_num)
        if resp.result != 0:
            print 'get rec req error'
            return -1
        for info in resp.video_list:
            obj = {}
            obj['category'] = '游戏'
            obj['vid']      = info.vid
            obj['good_num'] = info.video_praises
            obj['play_num'] = info.video_views
            t = TYPE_MAP.get(game_id)
            if not t:
                t = '热门'
            obj['second_c'] = t
            obj_map[info.vid] = obj

	print 'send v list:%s' % len(resp.video_list)
	req_num = resp.video_list
        result,v_info_list = get_videosInfo_req(udp_client, req_num)

        if result != 0:
            print 'get v_info req error'
            return -1

	print 'get info list:%s' % len(v_info_list)
        for info in v_info_list:
            v_obj = obj_map.get(info.vid)
            if not v_obj:
		print 'vid:%s has no info' % info.vid
                continue
            v_obj['title']    = info.custom_title
            v_obj['pic_url']  = info.url
            v_obj['duration'] = info.video_time
            for tag in info.tag_info:
                tags = v_obj.setdefault('tags', [])
                tags.append(tag)
		print tags
            resp = get_download_info_req(udp_client=udp_client, vid=info.vid)
            if not resp:
                print 'vid:%s download info is null.' % info.vid
                continue
            if len(resp.ul) and len(resp.cl):
                url = resp.ul[0]
                cl  = resp.cl[0]
                v_url = '%s%s?vkey=%s' % (url.url, resp.fn, cl.vkey)
                v_obj['v_url'] = v_url

            obj_arr.append(v_obj)

        from_num += len(req_num)
        batch -= 1
    return obj_arr

udp_client = UDPClient()
obj_arr = adjust_hero_v_info(udp_client=udp_client, game_id=1007039)
print obj_arr
udp_client.close()
