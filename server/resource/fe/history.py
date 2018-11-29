# -*- coding: UTF-8 -*-
import time
import datetime

def assemble_history_content(iter_uv_obj):
    obj_arr = []
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yestoday = (datetime.datetime.now() - datetime.timedelta(days =1)).strftime("%Y-%m-%d")

    date_map_obj_arr = {}
    for uv_obj in iter_uv_obj:
        if not uv_obj:
            continue
        date = time.strftime("%Y-%m-%d", time.localtime(uv_obj.timestamp))
        t = time.strptime(date, "%Y-%m-%d")
        date_ts = int(time.mktime(t))
        if date == today:
            date = '今天'
        elif date == yestoday:
            date = '昨天'

        date_arr_obj = date_map_obj_arr.setdefault(date_ts,{'date':date, 'arr':[]})

        obj = {}
        obj['id']    = uv_obj.video_id
        obj['title'] = uv_obj.video_obj.name
        obj['url']   = uv_obj.video_obj.url
        obj['cover'] = uv_obj.video_obj.cover
        obj['play_count'] = uv_obj.video_obj.play_count
        obj['good_count'] = uv_obj.video_obj.good_count
        obj['duration']   = uv_obj.video_obj.duration
        obj['w_duration'] = uv_obj.w_duration
        date_arr_obj['arr'].append(obj)


    #for date,arr_m in sorted_map.items():
    for k in sorted(date_map_obj_arr.keys(), reverse=True):
        date_arr_obj_tmp = date_map_obj_arr[k]
        item = {'name':date_arr_obj_tmp['date'],'itemList':date_arr_obj_tmp['arr']}
        obj_arr.append(item)

    return obj_arr
