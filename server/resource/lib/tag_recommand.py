#-*-coding:utf-8-*-
import random
import math
import time
import sys
import traceback
#sys.path.append('/usr/local/app/nb')
from dao.user_behavior import UserBehavior
from lib.log import get_logger
logger = get_logger('busi')
#统计各类数量  
def addValueToMat(theMat,key,value,incr):
    if key not in theMat: #如果key没出先在theMat中  
        theMat[key]=dict();
        theMat[key][value]=incr;
    else:
        if value not in theMat[key]:
            theMat[key][value]=incr;
        else:
            theMat[key][value]+=incr;#若有值，则递增  

user_tags = dict();
tag_items = dict();
user_items = dict();
user_items_test = dict();#测试集数据字典  
item_tags = dict()        #用于多样性测试

#初始化，进行各种统计  
def init_stat(usr):
    ub = UserBehavior(user=usr)
    try:
        for data in ub.get_behavior():
            user   = data[0]
            item   = data[1]
            tag    = data[2]
            weight = data[3]
            if not (user and item and tag and weight):
                continue
            addValueToMat(user_tags, user, tag, weight)
            addValueToMat(user_items, user, item, 1)

        for data in ub.get_all_items():
            item   = data[0]
            tag    = data[1]
            weight = data[2]
            addValueToMat(tag_items, tag, item, weight)
            addValueToMat(item_tags, item, tag, weight)

        return recommend(usr)
    except:
        logger.error('fail|exception|list_stat error|%s' % traceback.format_exc())
    finally:
        ub.close()

#推荐算法  
def recommend(user):
    recommend_list = dict()
    if not user_items.has_key(user) :
        logger.warn('no user item:%s, return' % user)
        return
    tagged_item = user_items[user]
    if not tagged_item:
        logger.info('user:%s has no items, return' % user)
        return
    #print tagged_item
    if not user_tags[user]:
        logger.info('user:%s has no tags, return' % user)
        return

    try:
        for tag_,wut in user_tags[user].items():
            if not tag_items.get(tag_):
                logger.error('tag:{} has no items'.format(tag_))
                continue
            for item_,wit in tag_items[tag_].items():
                if item_ not in tagged_item:
                    if item_ not in recommend_list:
                        recommend_list[item_] = wut*wit
                    else:
                        recommend_list[item_] += wut*wit
    except:
        logger.error('fail|exception|recommend error|%s' % traceback.format_exc())
    finally:
        return sorted(recommend_list.iteritems(), key = lambda a:a[1],reverse = True)


#计算余弦相似度
def cosine_sim(item_tags,i,j):
    ret = 0
    for b,wib in item_tags[i].items():     #求物品i,j的标签交集数目
        if b in item_tags[j]:
            ret += wib * item_tags[j][b]
    ni = 0
    nj = 0
    for b, w in item_tags[i].items():      #统计 i 的标签数目
        ni += w * w
    for b, w in item_tags[j].items():      #统计 j 的标签数目
        nj += w * w
    if ret == 0:
        return 0
    return ret/math.sqrt(ni * nj)          #返回余弦值       

#计算推荐列表多样性
def diversity(item_tags,recommend_items):
    ret = 0
    n = 0
    for i in dict(recommend_items).keys():
        for j in dict(recommend_items).keys():
            if i == j:
                continue
            ret += cosine_sim(item_tags,i,j)
            n += 1
    return ret/(n * 1.0)

def get_rec_list(top, user):
    recommend_list = init_stat(user)
    if recommend_list:
        for recommend in recommend_list[:top]:  #兴趣度最高的top itemid
            yield recommend

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    vid_arr = []
    for recommend in get_rec_list(10,'shawnsha'):  #兴趣度最高的十个itemid
        vid_arr.append("'" + recommend[0] + "'")
    print ','.join(vid_arr)


#推荐列表多样性,计算时间较长
#diversityNum = diversity(item_tags, recommend_list)
#print diversityNum
