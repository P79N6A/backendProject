from lib.log import get_logger

class Billboard(object):
    def __init__(self, base):
        self.base = base
        self.logger = get_logger('db')

    def get_billboard_info(self):
        sql = 'select * from t_billboard where f_id=(select max(f_id) from t_billboard)'
        val = self.base.exec_r_one(sql)
        if val:
            bb = _Billboard()
            bb.f_id   = val['f_id']
            bb.qr_url = val['qr_url']
            bb.notice = val['notice']
            bb.modify_time = val['modify_time']
            bb.modify_user = val['modify_user']

            return bb

    def add_billboard_info(self, qr_url, notice, modify_time,modify_user):
        sql = "insert into t_billboard(qr_url, notice, modify_user, modify_time) values (%s,%s,%s,%s)"
        self.base.exec_w(sql, qr_url, notice,modify_time, modify_user)

class _Billboard(object):
    def __init__(self, f_id=0, qr_url='', notice='', modify_user='',
                 modify_time=''):
        self.f_id = f_id
        self.qr_url = qr_url
        self.notice = notice
        self.modify_user = modify_user
        self.modify_time = modify_time
