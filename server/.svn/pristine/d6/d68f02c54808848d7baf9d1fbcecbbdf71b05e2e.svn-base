import commands
import MySQLdb
import os
import json
import sys

files= os.listdir('/data1/videos/1080P')

ffprobe_path = '/usr/local/app/bin/ffprobe'
ffprobe_args = '-v quiet -print_format json -show_format'
v_path = '/data1/videos/1080P/%s'

def get_video_info():
    items = []
    for v in files:
        video_path = v_path % v
        cmd = '%s %s %s' % (ffprobe_path,ffprobe_args,video_path)
        status,output = commands.getstatusoutput(cmd)
        data = json.loads(output)
        if data.has_key('format'):
            duration = int(float(data['format']['duration']) * 1000)
            sql = "update t_videos set duration=%s where h_id='%s'" % (duration,v.split('.')[0])
            items.append(sql)
    return items


if __name__ == "__main__":
    sqls = get_video_info()
    config = {
            'host': 'newbridge.mdb.mig',
            'port': 16850,
            'user': 'writeuser',
            'passwd': 'tQdg8ZnYoVjrx04J',
            'db': 'newbridge',
            'charset': 'utf8'
    }
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()
    for sql in sqls:
        print sql
        cursor.execute(sql)

    conn.commit()
    conn.close()
