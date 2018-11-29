#-*-coding:utf-8-*-
import random
import math
import time
import sys
import traceback
#sys.path.append('/usr/local/app/nb')
from dao.video_tag import VideoTag
from dao.music_tag import MusicTag
from lib.log import get_logger
from lib.config import read_db_config
logger = get_logger('music')
#统计各类数量  
#def addValueToMat(theMat,key,value,incr):
#    if key not in theMat: #如果key没出先在theMat中  
#        theMat[key]=dict();
#        theMat[key][value]=incr;
#    else:
#        if value not in theMat[key]:
#            theMat[key][value]=incr;
#        else:
#            theMat[key][value]+=incr;#若有值，则递增  

tag_items = dict()
item_tags = dict()

def rec_music(base):
    vt = VideoTag(base)
    mt = MusicTag(base)
    try:
        for data in vt.get_maxweigth_items():
            item   = data.video_id
            tag    = data.tag
            #weight = data.weight
            item_tags.setdefault(item, []).append(tag)

        for item,tags in item_tags.items():
            musics = set()
            for tag in tags:
                music_id = mt.get_music_id_by_tag(tag)
                if music_id:
                    musics.clear()
                    musics.add(music_id)
                if not music_id and not len(musics):
                    music_id = 'test'
                    musics.add(music_id)
            musics_str = ','.join(musics)
            logger.info('musics rec:%s->%s'%(item,musics_str))
            vt.add_music_recommend(item, musics_str)

    except:
        logger.error('fail|exception|list_stat error|%s' % traceback.format_exc())

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    rec_music()
