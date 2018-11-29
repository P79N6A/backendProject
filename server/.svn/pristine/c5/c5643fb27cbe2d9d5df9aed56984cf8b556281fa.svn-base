# -*- coding: UTF-8 -*-
from flask import Flask,g,jsonify,request
from lib.log import get_logger

from lib.route_handler import handle_success,handle_param_error,handle_failure,handle_response,check_param

#routers
from modules.medias import medias_service
from modules.login  import login_service
from modules.third_res import third_service
from modules.profile   import profile_service
from modules.chuan     import chuan_service
from modules.video     import video_service
from modules.menu      import menu_service
from modules.fans      import fans_service
from modules.hot_list  import hotlist_service
from modules.history   import history_service
from modules.dance     import dance_service
from modules.qrcode    import qrcode_service
#from modules.h5        import h5_service
from modules.notice    import notice_service

import sys
import traceback
import uuid
import tempfile
import json
import os
import time


logger = get_logger('main')
access = get_logger('access')
resp_logger = get_logger('response')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#register routers
app.register_blueprint(medias_service)
app.register_blueprint(login_service)
app.register_blueprint(third_service)
app.register_blueprint(profile_service)
app.register_blueprint(chuan_service)
app.register_blueprint(video_service)
app.register_blueprint(menu_service)
app.register_blueprint(fans_service)
app.register_blueprint(hotlist_service)
app.register_blueprint(history_service)
app.register_blueprint(dance_service)
app.register_blueprint(qrcode_service)
#app.register_blueprint(h5_service)
app.register_blueprint(notice_service)

reload(sys)
sys.setdefaultencoding('utf-8')


@app.route('/', methods=['POST','GET'])
def hi():
    return 'Hi'

@app.before_request
def before_request():
    g.uuid = uuid.uuid1().hex
    g.begin_ts = int(time.time() * 1000)
    req_data = save_request(g.uuid, request)
    access.info("Request: %s %s %s"%(request.method, request.path, request.endpoint))
    access.info("Request Data:%s"%json.dumps(req_data, indent=4))
    data = request.json
    if data:
        data = data.get("data")
        if not check_param(data):
            return handle_param_error()


@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    #resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    resp_data = save_response(g.uuid, g.begin_ts, resp)
    resp_logger.info('Response: %s', json.dumps(resp_data, indent=4))
    return resp

@app.errorhandler(404)
def page_not_found(e):
    return jsonify('Not Found')

def save_response(uuid, ts, resp):
    end_ts               = int(time.time() * 1000)
    resp_data = {}
    resp_data['elapsed'] = end_ts - ts
    resp_data['uuid']    = uuid
    resp_data['status_code'] = resp.status_code
    resp_data['status']  = resp.status
    resp_data['headers'] = dict(resp.headers)
    #resp_data['data']    = resp.data
    return resp_data

def save_request(uuid, request):
    req_data = {}
    req_data['uuid'] = uuid
    req_data['endpoint'] = request.endpoint
    req_data['method'] = request.method
    req_data['cookies'] = request.cookies
    req_data['data'] = request.data
    req_data['headers'] = dict(request.headers)
    req_data['headers'].pop('Cookie', None)
    req_data['args'] = request.args
    req_data['form'] = request.form
    req_data['remote_addr'] = request.remote_addr
    #files = []
    #for name, fs in request.files.iteritems():
    #    dst = tempfile.NamedTemporaryFile()
    #    fs.save(dst)
    #    dst.flush()
    #    filesize = os.stat(dst.name).st_size
    #    dst.close()
    #    files.append({'name': name, 'filename': fs.filename, 'filesize': filesize,
    #     'mimetype': fs.mimetype, 'mimetype_params': fs.mimetype_params})
    #req_data['files'] = files
    return req_data

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
