# -*- coding: UTF-8 -*-
import traceback
import hero.proto.ticketsvr_pb2 as pb_openid
import hero.proto.hero_time_pb2 as pb_hero

from l5.get_router import get_router
from lib.config import read_l5_info
from transport.client import UDPClient
from lib.log import get_logger
from hero.qt_herlper import QtHelper
from lib.config import read_link_domain

logger = get_logger('main')
Domain = read_link_domain()

def get_openid_by_uuid(uuid=0, uin=0):
    #need ask them l5.
    udp_client = UDPClient(host='10.239.196.159', port=15000)
    try:
        qt = QtHelper()
        sess = qt.createSessInfo(pb_openid.CMD_TICKETSVR,
                                 pb_openid.SUBCMD_PARSE_ID,
                                 8031,uin)

        req = pb_openid.ParseIdReq()
        req.ids.extend([uuid])

        res = qt.buildSendPkg(sess, req)

        udp_client.sendData(buf=res.serialize())
        bb = udp_client.recvData()

        resp = qt.parseReceivePkg(bb)
        resp.unserialize()
        resp_str = str(buffer(resp.body_str)[:])
        pb_resp = pb_openid.ParseIdRsp()
        pb_resp.ParseFromString(resp_str)
 
        return pb_resp
    except:
        logger.error('get error:%s'%traceback.format_exc())
    finally:
        udp_client.close()

def _uuid_to_openid(uuid):
    resp = get_openid_by_uuid(uuid=uuid)
    if not (resp and resp.infos):
        return None,None
    infos = resp.infos[0]
    id_type  = infos.id_type
    if id_type != 2:
        return None,None
    uid_type = infos.uuid_type
    openid = ''
    if uid_type == 1:
        openid = infos.uin
    elif uid_type == 2:
        openid = infos.commid

    return uid_type, openid


def assemble_v_obj(info, game_id, appid, flag=True):
    game_id = game_id or info.game_id
    game_id = int(game_id)
    v_obj = {}
    v_obj['title']    = info.custom_title.title
    v_obj['game_id']  = game_id
    v_obj['pic_url']  = info.url
    v_obj['duration'] = info.video_time * 1000
    v_obj['share_time'] = info.share_time
    v_obj['nickname']   = info.user_nick or ''
    v_obj['user_icon']  = info.user_icon
    v_obj['src_uid']    = info.uid
    v_obj['vid']      = info.vid
    v_obj['good_num'] = info.praise_num
    v_obj['play_num'] = info.video_views
    v_obj['nickname'] = info.user_nick or ''
    v_obj['user_icon']  = info.user_icon or ''
    v_obj['definition'] = 0
    v_obj['v_url'] = ''
    v_obj['category'] = ''
    v_obj['second_c'] = ''
    v_obj['appid']    = appid
    v_obj['tags']     = []

    try:
        uid_type,src_open_id = _uuid_to_openid(info.uid)
        #v_obj['uid']         = src_open_id
        v_obj['uid_type'] = uid_type
        v_obj['src_id']   = src_open_id
    except:
        logger.error('uuid to openid fail, ignore video item:%s'%v_obj['vid'])
        logger.error(traceback.format_exc())
        return None


    tag_info = pb_hero.GameTagInfo()
    tag_info.ParseFromString(info.tag_info)
    if len(tag_info.kv_list):
        for kv in tag_info.kv_list:
            v_obj.setdefault('tags', []).append(kv.key+kv.value)

    if flag:
        modid,cmdid = read_l5_info()
        host,port = get_router(modid, cmdid)
        if not (host and port):
            logger.error('l5 get error')
            return v_obj
        udp_client = UDPClient(host=host, port=port)

        v_url,definition = get_download_url_and_definition(vid=info.vid,game_id=game_id, udp_client=udp_client)
        #v_obj['v_url'] = v_url
        v_obj['v_url'] = ''
        v_obj['definition'] = definition

    return v_obj

def _convert_qq_uin_arr(uin_arr = []):
    if len(uin_arr):
        from openid_service.qq_openid_service import QQBinaryOpenidService
        open_s = QQBinaryOpenidService()

        logger.info('start convert uin to openid:%s'%(uin_arr))
        uin_openid_map  = open_s.qq_to_openid(uin_arr)
        if not (uin_openid_map and len(uin_openid_map)):
            logger.error('qq_to_openid fail, return None')
            return None
        logger.info('convert to newbridge openid finish, result:%s'%uin_openid_map)
        return uin_openid_map

def _convert_weinxin_openid_arr(openid_arr = []):
    if len(openid_arr):
        from lib.httptool import open_url_json
        data = {}
        data['target_appid'] = 'wx3566ceb82d2e0f2d'
        data['openid_list']  =  openid_arr
        tmp = open_url_json(url='http://%s/weixin/openid/convert'%Domain, data=data)
        if not (tmp and isinstance(tmp, dict) and tmp.get("data")):
            logger.error('convert uid to lpuid error, uid:%s lp_appid:%s'%(openid_arr,'wx3566ceb82d2e0f2d'))
            return None

        openid_map = tmp.get('data')
        if not (openid_map and len(openid_map)):
            logger.error('weixin_openid_to_openid return null, return None')
            return None
        logger.info('convert to newbridge openid finish, result:%s'%openid_map)
        return openid_map


def convert_uid(obj_arr):
    weixin_arr = []
    qq_arr     = []

    weixin_openid_arr = []
    qq_uin_arr = []
    for item in obj_arr:
        uid_type = item['uid_type']
        src_id   = item['src_id']

        if uid_type == 2 and src_id:
            weixin_arr.append(item)
            weixin_openid_arr.append(src_id)
        elif uid_type == 1 and src_id:
            qq_arr.append(item)
            qq_uin_arr.append(src_id)
        else:
            logger.error('uid_type:%s or src_id:%s error'%(uid_type, src_id))

    #convert openid->openid , uin -> openid
    #暂时不要QQ用户数据
    logger.info('start convert qq uin batch:%s'%qq_uin_arr)
    uin_openid_map = _convert_qq_uin_arr(qq_uin_arr)
    logger.info('finish convert qq uin batch, res:%s'%uin_openid_map)
    if uin_openid_map:
        for item in qq_arr:
            src_id = item['src_id']
            convert_id = uin_openid_map[src_id]

            logger.info('qq uin convert result:%s->%s'%(src_id, convert_id))
            item['uid'] = convert_id

    logger.info('start convert weixin openid batch:%s'%weixin_openid_arr)
    weixin_openid_map = _convert_weinxin_openid_arr(weixin_openid_arr)
    logger.info('finish convert weixin openid batch,res:%s'%weixin_openid_map)
    if weixin_openid_map:
        for item in weixin_arr:
            src_id = item['src_id']
            convert_id = weixin_openid_map[src_id]

            logger.info('weixin openid convert result:%s->%s'%(src_id, convert_id))
            item['uid'] = convert_id

    return weixin_arr,qq_arr


def get_download_url_and_definition(vid=0, game_id=0, udp_client=None):
    from common.tool import get_video_meta_info
    v_url = ''
    definition = ''
    resp = get_download_info_req(vid=vid,game_id=game_id, udp_client=udp_client)
    if not resp:
        logger.warn('vid:%s download info is null.' % vid)
        return v_url,definition
    if len(resp.ul) and len(resp.cl):
        url = resp.ul[0]
        cl  = resp.cl[0]
        v_url = '%s%s?vkey=%s' % (url.url, resp.fn, cl.vkey)
        v_meta_info = get_video_meta_info(v_url)
        if v_meta_info and v_meta_info.has_key('height'):
            definition = v_meta_info['height']
    else:
        logger.warn('[WARING] resp download info is null:%s.'%resp)


    return v_url,definition

def get_download_info_req(vid=0, platform=10, game_id=0,uin=0, udp_client=None):
    try:
        qt = QtHelper()
        sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                 pb_hero.SUBCMD_APPLY_DOWNLOAD_VIDEO,
                                 8031,uin)

        req = pb_hero.ApplyDownloadVideoReq()
        req.file_uuid = vid
        req.platform  = platform
        req.game_id   = game_id


        res = qt.buildSendPkg(sess, req)
        #b = res.serialize()

        udp_client.sendData(buf=res.serialize())
        bb = udp_client.recvData()

        resp = qt.parseReceivePkg(bb)
        resp.unserialize()
        resp_str = str(buffer(resp.body_str)[:])
        pb_resp = pb_hero.ApplyDownloadVideoRsp()
        pb_resp.ParseFromString(resp_str)

        return pb_resp
    except:
        logger.error('get error:%s'%traceback.format_exc())

