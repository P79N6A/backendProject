import sys
import traceback

from commonlib.dao.base import BaseDao
from commonlib.utils.log import get_logger
from commonlib.utils.config import read_db_config
from commonlib.utils.tool import get_now_ts_sec

logger = get_logger('session')

class SessionService(object):
    def __init__(self, base=None):
        self.base = base or BaseDao(read_db_config())

    def close(self):
        if self.base:
            self.base.close()
            self.base = None

    def _add_session(self, pool='default', k='', v='', expire=86400):
        if not (pool and k and v):
            logger.error('_add session error:need pool:%s and k:%s and v:%s'%(pool, k, v))
            return False
        sql = "replace into t_caches (`pool`,`k`,`v`, expire) values (%s,%s,%s,%s)"
        try:
            ts = get_now_ts_sec()  + expire
            self.base.exec_w(sql, pool, k, v, ts)
            logger.info('_add session success: pool:%s and k:%s and v:%s exp:%s'%(pool, k, v, ts))
            return True
        except:
            logger.error('_add session error:%s'%traceback.format_exc())
            return False

    def _get_session(self, pool='default', k=''):
        if not (pool and k):
            logger.error('_get session error:need pool:%s and k:%s'%(pool, k))
            return None

        sql = "select v, expire from t_caches where `pool`=%s and `k`=%s"
        try:
            vals = self.base.exec_r(sql, pool, k)
            if not (vals and len(vals)):
                logger.info('_get session fail, found no item, pool:%s, k:%s'%(pool, k))
                return None
            v      = vals[0]['v']
            expire = vals[0]['expire']
            now_ts = get_now_ts_sec()
            if now_ts > expire:
                logger.info('session expire, delete: pool:%s and k:%s'%(pool, k))
                self._delete_session(pool=pool, k=k)
                return None
            logger.info('_get session success: pool:%s and k:%s, v:%s'%(pool, k, v))
            return v
        except:
            logger.error('_add session error:%s'%traceback.format_exc())
            return None

    def _delete_session(self, pool='default', k=''):
        if not (pool and k):
            logger.error('_delete session error:need pool:%s and k:%s'%(pool, k))
            return False
        sql = "delete from t_caches where `pool`=%s and `k`=%s"
        try:
            self.base.exec_w(sql, pool, k)
            logger.info('_delete session success: pool:%s and k:%s'%(pool, k))
            return True
        except:
            logger.error('_delete session error:%s'%traceback.format_exc())
            return False


    def add_session(self, pool='default', k='', v='',expire=86400):
        logger.info('add session pool:%s, k:%s, v:%s, exp:%s'%(pool,k,v,expire))
        res = self._add_session(pool=pool,k=k,v=v,expire=expire)
        if res:
            logger.info('add session pool:%s, k:%s, v:%s success.'%(pool,k,v))
        else:
            logger.info('add session pool:%s, k:%s, v:%s fail.'%(pool,k,v))


    def get_session(self, pool='default', k=''):
        v = self._get_session(pool=pool, k=k)
        logger.info('get session pool:%s, k:%s, v:%s'%(pool,k,v))
        if v:
            logger.info('hit session, get value:%s'%v)
            return v

        return ''

    def clear_session(self, pool='default', k=''):
        logger.info('clear session pool:%s, k:%s'%(pool,k))
        res = self._delete_session(pool=pool, k=k)
        if res:
            logger.info('clear session pool:%s, k:%s success.'%(pool,k))
        else:
            logger.info('clear session pool:%s, k:%s fail.'%(pool,k))

if __name__ == "__main__":
    SessionService().add_session(k='test', v=11)
    print SessionService().get_session(k='test')

    SessionService().add_session(pool='test', k='test', v=11)
    print SessionService().get_session(pool='test',k='test')
    print SessionService().get_session(k='test')
    SessionService().close()
