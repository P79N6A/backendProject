import time
import random
from lib.config import read_video_url_config
from lib.config import read_cover_url_config
from lib.config import read_music_url_config


def assemble(v_info):
    obj = dict()
    obj['id']    = v_info.video_id
    obj['title'] = v_info.name
    obj['url']   = v_info.url
    obj['cover'] = v_info.cover
    obj['play_count'] = v_info.play_count
    obj['good_count'] = v_info.good_count
    obj['duration']   = v_info.duration
    obj['create_time'] = v_info.create_time
    obj['share_time']  = v_info.share_time
    obj['music_url']   = v_info.music_url
    obj['isHD']        = v_info.isHD
    obj['isMix']       = v_info.isMix
    obj['definition']  = v_info.definition
    obj['nickname']    = v_info.nickname
    obj['usericon']    = v_info.usericon
    obj['game_icon']   = v_info.game_icon
    obj['game_id']     = v_info.game_id
    return obj

def assemble_history(v_info,uv):
    obj = dict()
    obj['id']    = v_info.video_id
    obj['title'] = v_info.name
    obj['url']   = v_info.url
    obj['cover'] = v_info.cover
    obj['play_count'] = v_info.play_count
    obj['good_count'] = v_info.good_count
    obj['duration']   = v_info.duration
    obj['share_time']  = v_info.share_time

    obj['w_duration'] = uv.w_duration
    obj['timestamp']  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(uv.timestamp)))
    return obj

def get_video_obj(val):
    v = _Video()
    music_ids = val['music_ids'] if val.has_key('music_ids') else ''
    music_id  = music_ids.split(',')[0] if music_ids else ''
    v.f_id = val['f_id'] if val.has_key('f_id') else 0
    v.video_id = val['video_id'] if val.has_key('video_id') else 0
    v.name = val['name'] if val.has_key('name') else ''
    v.definition = val['definition'] if val.has_key('definition') else 0
    v.category   = val['category'] if val.has_key('category') else ''
    v.play_count = val['play_count'] if val.has_key('play_count') and val['play_count'] != 0 else random.randint(1,10)
    v.good_count = val['good_count'] if val.has_key('good_count') and val['good_count'] != 0 else random.randint(1,10)
    v.version    = val['version'] if val.has_key('version') else ''
    #v.src_type   = val['src_type'] if val.has_key('src_type') else 0
    v.create_time = val['create_time'] if val.has_key('create_time') else '0'
    v.share_time = val['share_time'] if val.has_key('share_time') else '0'
    v.url        = val['res_url'] if val.has_key('res_url') else ''
    v.cover      = val['pic_url'] if val.has_key('pic_url') else ''
    #v.url   = read_video_url_config(v)
    #v.cover = read_cover_url_config(v)
    v.duration   = val['duration'] if val.has_key('duration') else 0
    v.music_url  = read_music_url_config(music_id) if music_id else ''
    v.appid      = val['appid'] if val.has_key('appid') else 0
    v.uid        = val['uid'] if val.has_key('uid') else ''
    v.nickname   = val['nickname'] if val.has_key('nickname') else ''
    v.usericon   = val['user_icon'] if val.has_key('user_icon') else ''
    v.game_icon  = val['icon_url'] if val.has_key('icon_url') else ''
    v.game_id    = val['game_id'] if val.has_key('game_id') else 0
    v.isMix      = val['src_type'] == 2 if val.has_key('src_type') else False
    v.userid     = val['userid'] if val.has_key('userid') else 0
    v.isHD       = v.definition >= 1080

    return v

def get_hot_video_obj(val):
    v = _Video()

    v.cover       = val['pic_url'] if val.has_key('pic_url') else ''
    v.create_time = val['create_time'] if val.has_key('create_time') else '0'
    v.definition  = val['definition'] if val.has_key('definition') else 0
    v.duration    = val['duration'] if val.has_key('duration') else 0
    v.video_id    = val['video_id'] if val.has_key('video_id') else ''
    v.play_count  = val['play_count'] if val.has_key('play_count') and val['play_count'] != 0 else random.randint(1, 10)
    v.share_time  = val['share_time'] if val.has_key('share_time') else 0
    v.name        = val['name'] if val.has_key('name') else ''
    v.url         = val['res_url'] if val.has_key('res_url') else ''
    v.game_icon   = val['icon_url'] if val.has_key('icon_url') else ''
    v.game_id     = val['game_id'] if val.has_key('game_id') else 0
    v.userid      = val['userid'] if val.has_key('userid') else 0
    v.nickname    = val['nickname'] if val.has_key('nickname') else ''
    v.usericon    = val['user_icon'] if val.has_key('user_icon') else ''
    v.isMix       = val['src_type'] == 2 if val.has_key('src_type') else False
    v.isHD        = v.definition >= 1080

    return v

def assemble_adjuster(val):
    v = _Video()
    v.video_id = val['vid'] if val.has_key('vid') else 0
    v.name = val['title'] if val.has_key('title') else ''
    v.definition = val['definition'] if val.has_key('definition') else 0
    v.play_count = val['play_count'] if val.has_key('play_count') and val['play_count'] != 0 else random.randint(1,10)
    v.create_time = val['create_time'] if val.has_key('create_time') else '0'
    v.share_time = val['share_time'] if val.has_key('share_time') else '0'
    v.url        = val['res_url'] if val.has_key('res_url') else ''
    v.cover      = val['pic_url'] if val.has_key('pic_url') else ''
    v.duration   = val['duration'] if val.has_key('duration') else 0
    v.nickname   = val['nickname'] if val.has_key('nickname') else ''
    v.usericon   = val['user_icon'] if val.has_key('user_icon') else ''
    v.game_icon  = val['icon_url'] if val.has_key('icon_url') else ''
    v.game_id    = val['game_id'] if val.has_key('game_id') else 0
    v.uid        = val['uid'] if val.has_key('uid') else ''
    v.appid      = val['appid'] if val.has_key('appid') else 0
    v.userid     = val['userid'] if val.has_key('userid') else 0
    v.isMix      = False
    v.isHD       = v.definition >= 1080

    return v


class _Video(object):
    def __init__(self, f_id=0, name='', definition='', url='',
                 cover='',category='',play_count=100000,good_count=10000,
                 duration=0.0):
        self.f_id = f_id
        self.video_id = 0
        self.name = name
        self.definition = definition
        self.url   = url
        self.cover = cover
        self.play_count = play_count
        self.good_count = good_count
        self.category   = category
        self.duration   = duration
        self.version    = 'v100'
        self.create_time = 0
        self.share_time = 0
        self.music_url  = ''
        self.isHD = False
        self.isMix = False
        self.nickname = ''
        self.usericon = ''
        self.uid = ''
        self.appid = ''
        self.game_icon = ''
        self.game_id = 0
        self.userid = 0

    def toDict(self):
        dic                = {}
        dic['cover']       = self.cover
        dic['create_time'] = self.create_time
        dic['definition']  = self.definition
        dic['duration']    = self.duration
        dic['id']          = self.video_id
        dic['play_count']  = self.play_count
        dic['share_time']  = self.share_time
        dic['title']       = self.name
        dic['url']         = self.url
        dic['isHD']        = self.isHD
        dic['game_icon']   = self.game_icon
        dic['userid']      = self.userid
        dic['uid']         = self.uid
        dic['nickname']    = self.nickname
        dic['usericon']    = self.usericon
        dic['isMix']       = self.isMix
        dic['game_id']     = self.game_id
        return dic

