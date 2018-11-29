import traceback
import time
import schedule
import warnings
warnings.filterwarnings("ignore")

from adjuster.hero_adjuster import HeroAdjuster
from adjuster.updater import Updater
from l5.get_router import get_router
from transport.client import UDPClient
from busi.dao.base import BaseDao
from busi.dao.data import Video
from lib.log import get_logger
from lib.config import read_l5_info
from meta.games import GAME_MAP

logger = get_logger('main')
fetcher = get_logger('fetcher')
updater = get_logger('updater')
fixer = get_logger('fix')


modid,cmdid = read_l5_info()

def fetch_games_job():
    for k,v in GAME_MAP.items():
        fetch_job(game_id=k)

def update_games_job():
    for k,v in GAME_MAP.items():
        update_job(game_id=k)

def fix_job():
    fixer.info('start fix job')
    host,port = get_router(modid, cmdid)
    if not (host and port):
        print 'l5 get error'
        return

    udp_client = UDPClient(host=host, port=port)

    b = BaseDao()
    video_dao = Video(b)

    try:
        up = Updater(video_dao, udp_client)
        up.fix_definition()
    except:
        exstr = traceback.format_exc()
        updater.error('update fix error:%s' % exstr)
    finally:
        b.close()
    fixer.info('fix job finish.')

def fetch_job(game_id=1007039):
    fetcher.info('start fetch job,gameid:%s...' % game_id)
    host,port = get_router(modid, cmdid)
    if not (host and port):
        print 'l5 get error'
        return

    udp_client = UDPClient(host=host, port=port)
    hero_adjuster = HeroAdjuster(udp_client)
    b = BaseDao()
    video_dao = Video(b)
    batch = 5
    batch_num = 10
    from_num  = 0
    try:
        obj_arr = hero_adjuster.adjust(batch=batch,batch_num=batch_num,from_num=from_num,game_id=game_id)
        for item in obj_arr:
            video_dao.add_item(item)
            video_dao.add_video_game(item['vid'], game_id)

        fetcher.info('fetch job finish, game_id:%s' % game_id)
    except:
        fetcher.info('fetch job error:%s, game_id:%s' % (traceback.format_exc(),game_id))
    finally:
        udp_client.close()
        b.close()

def update_job(game_id=1007039):
    host,port = get_router(modid, cmdid)
    if not (host and port):
        print 'l5 get error'
        return
    b = BaseDao()
    video_dao = Video(b)
    udp_client = UDPClient(host=host, port=port)

    try:
        updater.info('start update job...')
        up = Updater(video_dao, udp_client)
        up.update_url(game_id=game_id)
        updater.info('update job finish.')
    except:
        exstr = traceback.format_exc()
        updater.error('update job error:%s' % exstr)
    finally:
        udp_client.close()
        b.close()

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #fetch_games_job()
    #update_games_job()
    #fix_job()
    schedule.every().hour.at(":05").do(fetch_games_job)
    schedule.every(60).minutes.do(fix_job)
    #schedule.every().day.at("00:00").do(update_games_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
