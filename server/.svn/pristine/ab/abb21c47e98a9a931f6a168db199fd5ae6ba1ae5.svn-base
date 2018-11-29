from lib.log import get_logger

class User(object):
    def __init__(self, base):
        self.base = base
        self.logger = get_logger('db')

    def get_user_info(self, mac_id='', android_id=''):
        sql = ''
	val = ''
        if mac_id and android_id:
            sql = "select f_id,user_id,name,profile,mac_id,android_id from t_users where mac_id=%s and android_id=%s"
	    val = self.base.exec_r_one(sql,mac_id, android_id)
        elif mac_id:
            sql = "select f_id,user_id,name,profile,mac_id,android_id from t_users where mac_id=%s"
	    val = self.base.exec_r_one(sql,mac_id)
        elif android_id:
            sql = "select f_id,user_id,name,profile,mac_id,android_id from t_users where android_id=%s"
	    val = self.base.exec_r_one(sql,android_id)
        else:
            self.logger.warn('need mac_id or android_id')
            return
        if val:
            user = _User()
            user.user_id = val['user_id']
            user.f_id    = val['f_id']
            user.profile = val['profile']
            user.name    = val['name']
            user.mac_id  = val['mac_id']
            user.android_id = val['android_id']

            return user

    def add_user_id(self, user_id, mac_id='', android_id=''):
        if not user_id:
            self.logger.warn('need user_id.')
            return
        sql = "insert into t_users(user_id,mac_id,android_id) values (%s,%s,%s)"
        self.base.exec_w(sql,user_id, mac_id, android_id)

class _User(object):
    def __init__(self, f_id=0, user_id='', name='', profile='', mac_id='',
                 android_id=''):
        self.f_id = f_id
        self.user_id  = user_id
        self.name = name
        self.profile = profile
        self.mac_id  = mac_id
        self.android_id = android_id
