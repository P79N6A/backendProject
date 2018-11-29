# -*- coding: UTF-8 -*-
import sys
sys.path.append('/usr/local/app/nb')
import traceback
import json
import time
import re
import warnings
warnings.filterwarnings("ignore")

from lib.log import get_logger
from flask import Flask,jsonify,request,make_response
from service.chuan import ChuanService
#modid,cmdid = read_l5_info()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
reload(sys)
sys.setdefaultencoding('utf-8')

logger = get_logger('main')
@app.route('/')
def hi():
    return 'Hi'

@app.route('/chuan/job/create', methods=['POST'])
def create_chuan_job():
    logger.info('rec a chuan request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    logger.info('data:%s'%data)
    if not valid(data):
        return handle_param_error()

    uid   = data.get('userid') or 0
    title = data.get('title') or 0
    #duration  = data.get('data').get('duration') or 0
    vids = data.get('video_ids') or []
    if not valid(data):
        logger.info('fail|userid or vid is null, return')
        return handle_param_error()

    if not (uid and vids and len(vids)):
        logger.info('fail|userid or vid is null, return')
        return handle_param_error()

    s = ChuanService()
    try:
        result = s.createJob(uid=uid, vids=vids, title=title)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|ub request serve success:%s'%res)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())
    finally:
        s.close()

    return res

@app.route('/chuan/job/query', methods=['POST'])
def query_chuan_job():
    logger.info('rec a query request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not valid(data):
        return handle_param_error()
    jid  = data.get('jobid') or 0
    uid  = data.get('userid') or 0
    if not (jid and uid):
        logger.info('fail|userid or vid is null, return')
        return handle_param_error()

    s = ChuanService()
    try:
        result = s.queryJob(jid=jid)
        res    = handle_success(result, 1000, '成功')
        logger.info('success|ub request serve success:%s'%res)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())
    finally:
        s.close()

    return res

@app.route('/chuan/job/doing/query', methods=['POST'])
def query_doing_chuan_job():
    #logger.info('rec a query doing chuan request')
    res  = {'code' : 1000, 'msg' : '成功'}
    data = request.json
    data = data.get('data')
    if not valid(data):
        return handle_param_error()
    uid  = data.get('userid') or 0

    s = ChuanService()
    try:
        result = s.queryDoingJob(uid=uid)
        res    = handle_success(result, 1000, '成功')
        #logger.info('success|ub request serve success:%s'%res)
    except:
        res = handle_failure()
        logger.error('fail|exception|ub request serve error|%s' % traceback.format_exc())
    finally:
        s.close()

    return res


def valid(data):
    if not isinstance(data, dict):
        return False
    uid  = data.get('userid') or 0
    if uid and not re.search('^[0-9]+$', str(uid)):
        return False

    jid  = data.get('jobid') or 0
    if jid and not re.search('^[0-9]+$', str(jid)):
        return False

    vids = data.get('video_ids')
    if vids and (not isinstance(vids, list) or not len(vids)):
        return False

    return True


def handle_success(data, return_code, msg):
    return handle_response(data, return_code, msg)

def handle_param_error():
    data = {}
    return handle_response(data, 1007, '请求参数错误')

def handle_failure():
    data = {}
    return handle_response(data, 1001, '系统忙，请稍后重试...')

def handle_response(data, return_code, msg):
    result         = {}
    result['code'] = return_code
    result['msg']  = msg
    result['data'] = data

    #logger.info('result => {0}'.format(result))

    text     = json.dumps(dict(result), ensure_ascii = False)
    length   = len(text.encode('utf-8'))
    response = make_response(text)

    response.headers['Content-Type']   = 'application/json; charset=utf-8'
    response.headers['Content-Length'] = length
    return response


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception



if __name__ == "__main__":
    from resolver.resolver import Resolver
    from video_processor.processor import VideoProcessor
    from uploader.uploader import Uploader
    from lib.config import read_l5_info
    from l5.get_router import get_router
    from transport.client import UDPClient
    from busi.dao.base import BaseDao
    from busi.dao.data import Video

    from busi.dao.common import assemble
    from busi.dao.common import valid

    modid,cmdid = read_l5_info()
    host,port = get_router(modid, cmdid)
    if not (host and port):
        logger.error('l5 get error')
        sys.exit(1)
    udp_client = UDPClient(host=host, port=port)
    b = BaseDao()
    try:

        resolver = Resolver()
        results = resolver.start()
        processor = VideoProcessor()
        for item in results:
            candidates = item['candidates']
            game_id    = item['cmd']['game_id']
            merge_info = processor.work(candidates)

            if not (merge_info and merge_info.get('file_path')):
                print 'merge fail, exit'
                sys.exit(1)

            file_path = merge_info.get('file_path')

            up = Uploader(file_path, 'mp4', udp_client)
            up_info = up.upload(addrtype=2, game_id=game_id)

            if up_info['status'] != 0:
                print 'upload merge_file fail'
                sys.exit(1)

            logger.info('sleep.....15s')
            time.sleep(15)
            assemble_obj = assemble(candidates, up_info, udp_client)
            if assemble_obj and valid(assemble_obj):
                #print assemble_obj
                video_dao = Video(b)
                video_dao.add_item(assemble_obj)
                video_dao.add_video_game(assemble_obj['vid'], game_id)

    except:
        print traceback.format_exc()
    finally:
        udp_client.close()
        b.close()
