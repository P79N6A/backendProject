import commands
import os
import json
import sys
import getopt
import traceback

ffprobe_path = 'ffprobe'
ffmpeg_path = 'ffmpeg'

photo_args = '-i %s -y -f mjpeg -ss %s -t 1 /data1/v_photos/%s.jpg'
convert_args = '-i %s -s hd%s -vcodec libx264 -crf 23 -c:a aac -strict -2 %s'
ffprobe_args = '-v quiet -print_format json -show_format'

convert_flv_args = '-i %s -c:v libx264 -crf 19 -strict experimental %s'

commpress_no_sound_args = '-i %s -y -vcodec libx264 -crf 21 -an %s'
#commpress_no_sound_args = '-i %s -y -vcodec copy -crf 21 -an %s'
merge_sound_args = '-i %s -i %s -y -vcodec copy -acodec aac -shortest %s'

v_path = '/data1/videos/new'

def commpress_no_sound(input_path, output_path):
    arg = commpress_no_sound_args % (input_path, output_path)
    cmd = '%s %s' % (ffmpeg_path, arg)
    print cmd
    status,output = commands.getstatusoutput(cmd)
    print status, output

def merge_sound(input_path, input_path_sound, output_path):
    arg = merge_sound_args % (input_path, input_path_sound, output_path)
    cmd = '%s %s' % (ffmpeg_path, arg)
    print cmd
    status,output = commands.getstatusoutput(cmd)
    print status, output

def commpress_and_merege(input_path, input_path_sound, output_path, temp_path):
    commpress_no_sound(input_path, '%s/temp.mp4'%temp_path)
    merge_sound('%s/temp.mp4'%temp_path, input_path_sound, output_path)

def main_compress_and_merge():
    video_name = 'MVI_747133333.MOV'
    name = video_name.split('.')[0]

    temp_path = '/Users/shawn/Documents/video/merge'

    input_video = '/Users/shawn/Documents/video/dance/%s'%video_name
    input_music = '/Users/shawn/Documents/video/music/stos.mp3'
    out_video   = '%s/%s.mp4'%(temp_path,name)

    commpress_and_merege(input_video, input_music, out_video, temp_path)

def main_merge_sound():
    input_video = '/Users/shawn/Documents/video/merge/MVI_747133333.mp4'
    input_path_sound = '/Users/shawn/Documents/video/music/stos.mp3'
    out = '/Users/shawn/Documents/video/merge/temp.mp4'
    merge_sound(input_video, input_path_sound, out)

def convert_flv(hids, src_def):
    path = '%s/%s/' % (v_path, src_def) + '%s'
    for v in hids:
        video_path = path % v
        cmd = '%s %s %s' % (ffmpeg_path,convert_flv_args,video_path)
        status,output = commands.getstatusoutput(cmd)
        if not status:
            print 'convert_defination error:%s:%s' % (name, output)

def set_duration(hids, src_def):
    items = []
    path = '%s/%s/' % (v_path, src_def) + '%s'
    for v in hids:
        video_path = path % v
        cmd = '%s %s %s' % (ffprobe_path,ffprobe_args,video_path)
        status,output = commands.getstatusoutput(cmd)
        data = json.loads(output)
        if data.has_key('format'):
            duration_s = float(data['format']['duration'])
            duration_ms = int(duration_s * 1000)
            vid = v.split('.')[0]
            sql = "update t_videos set duration=%s where h_id='%s'" % (duration_ms,vid)
            items.append(sql)

    config = {
            'host': 'newbridge.mdb.mig',
            'port': 16850,
            'user': 'writeuser',
            'passwd': 'tQdg8ZnYoVjrx04J',
            'db': 'newbridge',
            'charset': 'utf8'
    }
    import MySQLdb
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()
    try:
        for sql in items:
            print sql
            cursor.execute(sql)

        conn.commit()
    except:
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


def get_photos(hids, src_def):
    path = '%s/%s/' % (v_path, src_def) + '%s'
    for v in hids:
        video_path = path % v
        cmd = '%s %s %s' % (ffprobe_path,ffprobe_args,video_path)
        status,output = commands.getstatusoutput(cmd)
        data = json.loads(output)
        if data.has_key('format'):
            duration_s  = float(data['format']['duration'])
            duration_ms = int(duration_s * 1000)
            vid = v.split('.')[0]
            photo_arg = photo_args % (video_path, int(duration_s/5), vid)
            photo_cmd = "%s %s" % (ffmpeg_path, photo_arg)
            print photo_cmd
            status,output = commands.getstatusoutput(photo_cmd)

def convert_defination(hids, src_def, tg_def):
    for name in hids:
        input_path = '%s/%s/%s' % (v_path, src_def, name)
        output_path = '%s/%s/%s' % (v_path, tg_def, name)
        arg = convert_args % (input_path, tg_def[:-1], output_path)
        cmd = '%s %s' % (ffmpeg_path, arg)
        status,output = commands.getstatusoutput(cmd)
        if not status:
            print 'convert_defination error:%s:%s' % (name, output)

def main(argv):
    func = None
    src_def = ''
    tg_def = ''
    tool = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["tool=", "src_def=", "tg_def="])
    except getopt.GetoptError:
        print 'python tool.py --tool --src_def --tg_def -i -o'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python tool.py --tool --src_def --tg_def -i -o'
            sys.exit()
        elif opt in ("--tool"):
            tool = arg
        elif opt in ("-i", "--src_def"):
            src_def = arg
        elif opt in ("-o", "--tg_def"):
            tg_def = arg

    if not tool:
        sys.exit(1)

    files= os.listdir('%s/%s' % (v_path, src_def))
    if tool == "convert":
        if not (src_def and tg_def):
            print 'err:need src_def and tg_def'
            sys.exit(1)

        convert_defination(files, src_def, tg_def)
    elif tool == "photo":
        if not src_def:
            print 'err:need src_def'
            sys.exit(1)

        get_photos(files, src_def)
    elif tool == "duration":
        if not src_def:
            print 'err:need src_def'
            sys.exit(1)

        set_duration(files, src_def)

if __name__ == "__main__":
    #main(sys.argv[1:])
    #main_compress_and_merge()
    main_merge_sound()
