# -*- coding: UTF-8 -*-
import sys
#sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/engine')
import uuid
import os
import random
import commands
import traceback
from subprocess32 import STDOUT, check_output
import shlex

from lib.config import read_path_config
from lib.log import get_logger
from busi.dao.common import get_pic_by_gameid

TIMEOUT = 6000

ffmpeg_path = 'ffmpeg'
logger = get_logger('ffmpeg')

#image_to_video = "-loop 1 -i '%s' -c:v libx264 -t %s -pix_fmt yuv540p -vf scale=960:540 %s"
image_to_video = "-y -loop 1 -i '%s' -t %s -vf scale={0}:{1} %s"
#ffmpeg -loop 1 -i pic.png -c:v libx264 -t 3 -pix_fmt yuv420p -vf scale=1920:1080 pic.mp4
cutout_video_simple_arg    = """-y -i '%s' -vcodec copy -acodec copy %s"""
cutout_video_long_time_arg = """-y -i '%s' -vf scale={0}:{1} -acodec copy %s"""
#cutout_video   = """-y -i '%s' -i '%s' -preset fast -filter_complex "[0:v][1:v] overlay=x=((main_w-overlay_w)/(main_w-overlay_w) + 10):y=(main_h-overlay_h - 40),drawtext=fontsize=20:fontfile=font/simsun.ttc:text='{0}':fontcolor='white':x=10:y=h-th-20,scale=1920:1080" -acodec copy %s"""
#ffmpeg -y -ss 00:00:00 -t 00:00:30 -i input.mp4 -vcodec copy -acodec copy output.mp4
merge_videos   = "-y -f concat -safe 0 -protocol_whitelist 'file,http,https,tcp,tls' -i '%s' -c copy %s"
#eg: ffmpeg -f concat -safe 0 -protocol_whitelist "file,http,https,tcp,tls" -i videos.txt -c copy output.mp4
convert_ts     = " -y -i '%s' -c copy -bsf:v h264_mp4toannexb -f mpegts %s"

merge_ts       = "cat %s/*.ts > %s"
#ts_to_video    = " -y -i '%s' -acodec copy -vcodec copy %s"
ts_to_video    = " -y -i '%s' -c copy -bsf:a aac_adtstoasc %s"


class VideoProcessor(object):
    def __init__(self):
        self.root_path = read_path_config(pathname='root')
        logger.info('root_path:%s' % self.root_path)
        self.workspace = '{0}/video/%s'.format(self.root_path)
        self.ts_path  = '{0}/video/%s/ts'.format(self.root_path)
        self.pic_path = '{0}/pic/%s'.format(self.root_path)
        self.tmp_path = ''

    def work(self, video_objs=None):
        try:
            merge_info = {}
            uid = str(uuid.uuid1())
            self.tmp_path = self.workspace % uid
            self.ts_path = self.ts_path % uid
            logger.info('mkdir:%s'%self.tmp_path)
            logger.info('mkdir:%s'%self.ts_path)
            os.makedirs(self.tmp_path, 0755);
            os.makedirs(self.ts_path, 0755);

            ts_file = self.init_input_ts(video_objs)
            if ts_file:
                output_file = '%s/%s.mp4' % (self.tmp_path, 'merge')
                if self.ts_to_video(ts_file, output_file):
                    merge_info['file_path'] = output_file
                    merge_info['workspace'] = self.tmp_path

                return merge_info
            else:
                return None
        except:
            logger.error(traceback.format_exc())
            return None

    def ts_to_video(self, input_file, output_file):
        ts_to_video_arg = ts_to_video % (input_file, output_file)
        ts_to_video_cmd = "%s %s" % (ffmpeg_path, ts_to_video_arg)
        logger.info('ts_to_video_cmd:%s'% ts_to_video_cmd)
        #status,output = commands.getstatusoutput(ts_to_video_cmd)
        cmd_args = shlex.split(ts_to_video_cmd)
        try:
            output = check_output(cmd_args, stderr=STDOUT, timeout=TIMEOUT)
        except:
            logger.error(traceback.format_exc())
            return False

        #if status:
        #    #logger.error('%s pic_to_video error:%s'% (pic_to_video_cmd, output))
        #    print '%s pic_to_video error:%s'% (ts_to_video_cmd, output)
        #    return False

        return True


    def videos_to_ts(self, input_files, output_path):
        index = 0
        output_file = '%s/all.ts' % output_path 
        for file_path in input_files:
            convert_ts_arg = convert_ts % (file_path, '%s/%s%s' % (output_path, index, 'tmp.ts'))
            convert_ts_cmd = '%s %s' % (ffmpeg_path, convert_ts_arg)
            logger.info('convert_ts_cmd:%s'% convert_ts_cmd)
            cmd_args = shlex.split(convert_ts_cmd)
            try:
                output = check_output(cmd_args, stderr=STDOUT, timeout=TIMEOUT)
            except:
                logger.error(traceback.format_exc())
                return False

            #status,output = commands.getstatusoutput(convert_ts_cmd)
            #if status:
            #    #logger.error('%s pic_to_video error:%s'% (pic_to_video_cmd, output))
            #    print '%s convert_ts_cmd error:%s'% (convert_ts_cmd, output)
            #    return False
            index += 1

        status,output = commands.getstatusoutput(merge_ts % (output_path, output_file))
        #cmd = merge_ts % (output_path, output_file)
        #cmd_args = shlex.split(cmd)
        #try:
        #    output = check_output(cmd_args, stderr=STDOUT, timeout=60)
        #except:
        #    print traceback.format_exc()
        #    return False

        if status:
            #logger.error('%s pic_to_video error:%s'% (pic_to_video_cmd, output))
            logger.error('%s merge_ts error:%s'% (merge_ts, output))
            return False
 
        return output_file



    def get_pic_by_video(self, video_obj):
        return self.pic_path % 'bbb.jpg'

    def pic_to_video(self, arg, pic_file, output_file):
        pic_to_video_arg = arg % (pic_file, 3, output_file)
        pic_to_video_cmd = "%s %s" % (ffmpeg_path, pic_to_video_arg)
        logger.info('pic_to_video_cmd:%s'% pic_to_video_cmd)
        #status,output = commands.getstatusoutput(pic_to_video_cmd)
        cmd_args = shlex.split(pic_to_video_cmd)
        try:
            output = check_output(cmd_args, stderr=STDOUT, timeout=TIMEOUT)
        except:
            logger.error(traceback.format_exc())
            return False

        return True

    def merge_videos(self, videos_file, output_file):
        merge_video_arg = merge_videos % (videos_file, output_file)
        merge_video_cmd = '%s %s' % (ffmpeg_path, merge_video_arg)
        logger.info('merge_video_cmd:%s'% merge_video_cmd)
        cmd_args = shlex.split(merge_video_cmd)
        try:
            output = check_output(cmd_args, stderr=STDOUT, timeout=TIMEOUT)
        except:
            logger.error(traceback.format_exc())
            return False

        return True

    def cutout_video(self, arg, input_file, output_file, username, user_icon):
        #tmp_icon = 'http://thirdwx.qlogo.cn/mmopen/vi_32/Bo3IJYvvYktLVn5GztnAlJgaeKEB1STicBcat8icYxM57krrTt9DYxTc4S2XUhXzavAic92Bia4DSgwLTcguDXDMDA/132'
        #user_icon = 'http://thirdwx.qlogo.cn/mmopen/vi_32/Bo3IJYvvYktLVn5GztnAlJgaeKEB1STicBcat8icYxM57krrTt9DYxTc4S2XUhXzavAic92Bia4DSgwLTcguDXDMDA/132'
        #cutout_video_arg = cutout_video % ('00:00:00', '00:00:30', input_file, user_icon, output_file)
        #cutout_video_arg = cutout_video % (input_file, user_icon, output_file)
        cutout_video_arg = arg % (input_file, output_file)
	#cutout_video_arg = cutout_video_arg.format(username.decode('utf-8'))

        cutout_video_cmd = "{0} {1}".format(ffmpeg_path, cutout_video_arg)
        logger.info(cutout_video_cmd)
        cmd_args = shlex.split(cutout_video_cmd)
        try:
            output = check_output(cmd_args, stderr=STDOUT, timeout=TIMEOUT)
        except:
            logger.error(traceback.format_exc())
            return False
        #if status:
        #    #logger.error('%s cutout error:%s'% (cutout_video_cmd, output))
        #    print '%s cutout error:%s'% (cutout_video_cmd, output)
        #    return False

        return True


    def init_input_ts(self, video_objs):
        video_files = []
        definitions = set()
        max_definition = 0
        for video_obj in video_objs:
            if not video_obj.definition:
                continue
            definitions.add(video_obj.definition)
            if video_obj.definition > max_definition:
                max_definition = video_obj.definition

        if max_definition == 0:
            max_definition = 1080

        image_to_video_arg = image_to_video.format(int(max_definition)/9*16, max_definition)

        cut_arg = ''
        if len(definitions) > 1:
            cut_arg = cutout_video_long_time_arg.format(int(max_definition)/9*16, max_definition)
        else:
            cut_arg = cutout_video_simple_arg


        for video_obj in video_objs:
            output_file = '%s/%s.mp4' % (self.tmp_path, video_obj.video_id)
            if self.cutout_video(cut_arg, video_obj.url, output_file, video_obj.nickname, video_obj.user_icon):
                video_files.append(output_file)
            else:
                logger.error('url:%s input error'% (video_obj.url))

        lst_dst = []
        video_num = len(video_files)
        pic_num   = video_num / 2
        index_lst = []

        while len(index_lst) < pic_num:
            pic_seed  = random.randint(0, video_num - 1)
            if pic_seed in index_lst:
                continue
            index_lst.append(pic_seed)

        index_lst = sorted(index_lst)
        index = 0
        for item in video_files:
            if len(index_lst) and index == index_lst[0]:
                video_obj = video_objs[index]
                #pic_file  = self.get_pic_by_video(video_obj)
                pic_file  = get_pic_by_gameid(game_id=video_obj.game_id)
                output_file = '%s/%s.mp4' % (self.tmp_path, video_obj.video_id+'_pic')
                if self.pic_to_video(image_to_video_arg, pic_file, output_file):
                    lst_dst.append(output_file)
                index_lst.pop(0)
            lst_dst.append(item)
            index += 1

        allts = self.videos_to_ts(lst_dst, self.ts_path)

        return allts



    #def init_input(self, video_objs):
    #    uid = str(uuid.uuid1())
    #    self.tmp_path = self.tmp_path % uid
    #    os.makedirs(self.tmp_path, 0755);
    #    video_files = []
    #    video_files_finnal = []
    #    for video_obj in video_objs:
    #        output_file = '%s/%s.mp4' % (self.tmp_path, video_obj.video_id)
    #        if self.cutout_video(video_obj.url, output_file, video_obj.user_icon):
    #            video_files.append(output_file)
    #            video_files_finnal.append(output_file)
    #    
    #    video_num = len(video_files)
    #    for i in range(video_num / 2):
    #        pic_seed  = random.randint(0, video_num - 1)
    #        video_obj = video_objs[pic_seed]
    #        pic_file  = self.get_pic_by_video(video_obj)
    #        output_file = '%s/%s.mp4' % (self.tmp_path, video_obj.video_id+'_pic')
    #        if self.pic_to_video(pic_file, output_file):
    #            video_files_finnal.insert(pic_seed, output_file)

    #    merge_file = '%s/files.txt' % self.tmp_path
    #    with open(merge_file, 'w') as f:
    #        for item in video_files_finnal:
    #            f.write("%s '%s'%s"%('file', item, os.linesep))
 
    #    return merge_file

class Video(object):
    pass

if __name__ == "__main__":
    obj1 = Video()
    obj1.video_id = '67a95fef208949a5bdc7adfaadcc480b'
    obj1.url = 'http://123.151.149.71/vpvp.tc.qq.com/1051_67a95fef208949a5bdc7adfaadcc480b.f0.mp4?vkey=D919CF90DDB2DA8DB7CE20F11D0E9396589FA968FF097E0DEF85B291D4276FBF9371D578BCDE110C7EB440092A64778923E85DDA95CB33774098D8CAF9BE8C1624190EEB6F8F69E6E6D85BEDEE4536E16D7FE2C656A737A5&definition=540P'
    obj2 = Video()
    obj2.video_id = 'ebdfe5e614e84708b465a57b251850b9'
    obj2.url = 'http://123.151.65.15/vpvp.tc.qq.com/1051_ebdfe5e614e84708b465a57b251850b9.f0.mp4?vkey=E7C60E760004EB17A6EA46F697858C77F4EAE4AC49C2712460AF789E5390F6D3190BE633B3CB411AE619C4DE8F8B99C6B1A16DA727B887FA8F6B029A5898467215D6C65548B07C95C06E62957C409179FBDB675720636EED&definition=540P'
    videos = [obj1, obj2]
    processor = VideoProcessor()
    processor.work(videos)
