import time

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

    obj['w_duration'] = uv.w_duration
    obj['timestamp']  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(uv.timestamp)))
    return obj
