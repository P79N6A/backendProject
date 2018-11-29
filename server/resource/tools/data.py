# -*- coding: UTF-8 -*-
import csv
import MySQLdb
import sys
import traceback
import urllib
from sys import argv
import pandas as pd
import numpy as np


tags = set();
categorys = set();


def add_dic_tag_data(data):
    try:
        if data[0]:
            sql = "replace into dic_tag_data " +\
            "(idx,name,tag_name,content_id) values" +\
            "('%s','%s','%s','%s')"% (data[0], data[1], data[2], data[3])
            print sql
            cursor.execute(sql)
    except:
        print "addVideos error:", sys.exc_info()[0]
        raise
    finally:
        pass


def add_videos(data):
    try:
        if data[0]:
            sql = "replace into t_videos" +\
            "(h_id,en_name,name,definition,res_url,duration,version) values" +\
            "('%s','%s','%s','%s','%s',0,'%s')"\
                    % (data[0], data[1], data[2], data[3], data[4], data[5])
            print sql
            cursor.execute(sql)
    except:
        print "addVideos error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_categorys(data):
    try:
        if data[6] not in categorys:
            if data[6]:
                categorys.add(data[6])
                sql = "replace into t_categorys (name) values ('%s')" % (data[6])
                print sql
                cursor.execute(sql)
    except:
        print "add categorys error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_tags(data):
    tmp = []
    tmp_d = []
    for i in range(8,19,2):
        if data[i] and data[i] not in tags:
            tmp.append("('%s')" % data[i])
            tmp_d.append("'%s'" % data[i])
            tags.add(data[i])
    try:
	if tmp and tmp_d:
            sql = "replace into t_tags (name) values %s" % (','.join(tmp))
            print 'addTags',sql
            cursor.execute(sql)
    except:
        print "add tags error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_video_categorys(data):
    try:
        if data[0] and data[6]:
            sql = "replace into t_video_categorys (video_id,category) values ('%s','%s')" % (data[0], data[6])
            print 'add_video_categorys', sql
            cursor.execute(sql)
    except:
        print "addVideosCategorys error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_video_second_categorys(data):
    try:
        if data[0] and data[7]:
            sql = "replace into t_video_categorys (video_id,category,layer) values ('%s','%s',1)" % (data[0],data[7])
            print 'add_video_second_categorys', sql
            cursor.execute(sql)
    except:
        print "addVideosSecondCategorys error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_categorys_map(data):
    try:
        if data[6] and data[7]:
            sql = "replace into t_category_childrens (f_f_category,f_c_category,layer) values ('%s','%s',0)" %\
            (data[6],data[7])
            print 'add_video_second_categorys', sql
            cursor.execute(sql)
    except:
        print "addCategoryMap error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_video_tags(data):
    try:
        for i in range(8,19,2):
            if data[0] and data[i]:
                weight = data[i+1] or 1
                sql = "replace into t_video_tags (video_id,tag,weight) values ('%s','%s',%s)" \
                % (data[0], data[i], weight)
                print sql
                cursor.execute(sql)
    except:
        print "addVideoTags error:", sys.exc_info()[0]
        raise
    finally:
        pass

def add_media_video(data, t):
    try:
        if data and t:
            duration = data[5] or 0
            args = (data[0], data[1], data[2], data[3], data[4], duration, data[6], t)
            args = args + args[:-1]
            sql = """
            insert into t_medias(url,player,name,media_id,user_id,duration,pic_url,type)
            values ('%s','%s','%s','%s',%s,%s,'%s', %s)
            ON DUPLICATE KEY UPDATE url='%s',player='%s',name='%s',media_id='%s',user_id=%s,duration=%s,pic_url='%s'
            """% tuple(args)
            print sql
            cursor.execute(sql)
    except:
        print traceback.format_exc()
    finally:
        pass

def add_dance_music(data, t):
    try:
        if data and t:
            args = (data[0], data[1], data[2], data[3], data[6], 30000)
            args = args + args
            sql = """
            insert into t_dance_music(url,player,name,music_id,pic_url,high_duration)
            values ('%s','%s','%s','%s', '%s', %s)
            ON DUPLICATE KEY UPDATE url='%s',player='%s',name='%s',music_id='%s',pic_url='%s',high_duration=%s
            """% tuple(args)
            print sql
            cursor.execute(sql)
    except:
        print traceback.format_exc()
    finally:
        pass


def add_dance_work(data):
    try:
        if data:
            csv_data = ''
            player_num = data[9] or 1
            try:
                f = open(data[8])
                csv_data = f.read()
            except:
                print 'read :%s error,ignore data'%data[8]

            if csv_data:
                sql = """
                    insert into t_dance_works(dance_music_id,video_id,user_id,data,player_num) values('%s', '%s', %s, '%s',%s)
                    ON DUPLICATE KEY UPDATE data='%s', player_num=%s
                """ % (data[7], data[3], data[4], csv_data, player_num, csv_data, player_num)
            else:
                sql = """
                    insert into t_dance_works(dance_music_id,video_id,user_id,player_num) values('%s', '%s', %s, %s)
                    ON DUPLICATE KEY UPDATE player_num=%s
                """ % (data[7], data[3], data[4], player_num, player_num)

            print sql
            cursor.execute(sql)

    except:
        print traceback.format_exc()

    finally:
        pass

def add_video_game(data, game_id):
    try:
        if data and game_id and data[3]:
            sql = """
                insert ignore into t_video_game(video_id,game_id) values('%s', %s)
            """ % (data[3], game_id)
            print sql
            cursor.execute(sql)

    except:
        print traceback.format_exc()

    finally:
        pass

def _add_media_photo(data):
    if len(data) >= 9:
        add_media_video(data, 1)
        #add_user_media(data)
    else:
        print 'err: len data < 9'

def _add_dance_music(data):
    if len(data) >= 9:
        add_dance_music(data, 2)
    else:
        print 'err: len data < 9'


def _add_media_dance_video(data):
    if len(data) >= 9:
        add_media_video(data, 3)
        #add_user_media(data)
        add_dance_work(data)
        add_video_game(data, 1000001)
    else:
        print 'err: len data < 9'




def clear():
    tables = ['t_video_tags','t_category_childrens','t_categorys','t_tags','t_video_categorys']
    for table in tables:
        try:
            sql = "delete from %s" % table
            cursor.execute(sql)
        except:
            print "delete data error:%s" % sql, sys.exc_info()[0]
            raise
        finally:
            pass

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #读取文件
    #f = open("temp.txt")
    url = argv[1]
    urllib.urlretrieve(url, "copy.xlsx")
    df = pd.read_excel('copy.xlsx')

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
    try:
        #clear()
        while 1:
            line = f.readline()
            if not line:
                f.close()
                break
            data = line.split('\t')
            for i in range(len(data)):
		        data[i] = data[i].strip()

            #_add_media_dance_video(data)
            #_add_media_photo(data)
            _add_dance_music(data)

            #add_dic_tag_data(data)
            #add_videos(data)
            #add_categorys(data)
            #add_tags(data)
            #add_video_categorys(data)
            #add_video_tags(data)
            #add_video_second_categorys(data)
            #add_categorys_map(data)
        conn.commit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
	conn.rollback()
        raise
    finally:
        f.close()
        cursor.close()
        conn.close()
