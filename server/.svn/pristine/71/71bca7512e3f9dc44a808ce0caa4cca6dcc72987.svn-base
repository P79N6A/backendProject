# -*- coding: UTF-8 -*-
import time

from busi.dao.data import VideoInfo
from busi.dao.base import BaseDao
from busi.dao.data import Video
from l5.get_router import get_router
from transport.client import UDPClient
from lib.config import read_l5_info
from lib.config import read_appid
from lib.log import get_logger

logger = get_logger('uploader')

def get_second_c_by_gameid(game_id=0):
    b = BaseDao()
    video_dao = Video(b)
    name = video_dao.get_content_by_game_id(game_id)
    b.close()

    return name

def get_pic_by_gameid(game_id=0):
    pic_map = {
        1007058 : 'http://beta.myapp.com/myapp/LRS/nb/role/chiji.jpg',
        1007039 : 'http://beta.myapp.com/myapp/LRS/nb/role/libai.png',
        1007060 : 'http://beta.myapp.com/myapp/LRS/nb/role/feiche.jpeg'
    }
    default = 'http://beta.myapp.com/myapp/LRS/nb/role/tgp.jpeg'
    val = pic_map[int(game_id)] or default
    return val

def assemble(src_video_objs, merge_info, udp_client):
    from adjuster.adjuster_tool import get_download_url_and_definition

    if not (src_video_objs and merge_info and udp_client):
        return None
    tags = []
    duration = 0
    for obj in src_video_objs:
        if isinstance(obj, VideoInfo):
            tags.extend(obj.tags)
            duration += obj.duration


    game_id  = merge_info['game_id']
    #vid_list = [merge_info['vid']]
    #obj_arr = hero_adjuster.get_video_info_by_vid_list(vid_list=vid_list, game_id=game_id)
    #if not (obj_arr and len(obj_arr)):
    #    logger.warn('video_infos is null, vids:%s'%vid_list)
    #    return None
    #obj = obj_arr[0]

    v_url,definition = get_download_url_and_definition(vid=merge_info['vid'],game_id=game_id,udp_client=udp_client)
    ts = long(time.time()) 
    v_obj = {}
    v_obj['title']    = '【串烧合集】: %s' % get_second_c_by_gameid(game_id = game_id)
    v_obj['vid']      = merge_info['vid']
    v_obj['pic_url']  = get_pic_by_gameid(game_id=game_id)
    v_obj['duration'] = duration
    v_obj['share_time'] = ts
    v_obj['nickname']   = 'newbridge'
    v_obj['user_icon']  = 'http://beta.myapp.com/myapp/LRS/nb/game_icon/wz.png'
    v_obj['uid']       = '289296918'
    v_obj['good_num'] = 0
    v_obj['play_num'] = 0
    v_obj['definition'] = definition or 0
    v_obj['v_url']      = v_url or ''
    v_obj['tags']       = tags
    v_obj['appid']      = read_appid()
    #v_obj['appid']      = 'wx3566ceb82d2e0f2d'
    #v_obj['second_c'] = get_second_c_by_gameid(game_id) or '热门游戏'
    v_obj['second_c'] = '串烧'
    v_obj['category'] = '游戏'
    v_obj.setdefault('tags', []).append(v_obj['second_c'])

    return v_obj


def valid(assemble_obj):
    return True
