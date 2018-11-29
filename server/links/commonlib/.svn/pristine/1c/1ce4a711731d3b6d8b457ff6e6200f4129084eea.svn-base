import MySQLdb
import traceback
from commonlib.utils.config import read_db_config
from commonlib.utils.log import get_logger
logger = get_logger('db')

class BaseDao(object):
    def __init__(self, conf=read_db_config()):
        self.conn = MySQLdb.connect(**conf)
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def exec_r(self, sql, *args):
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchall()
        except:
            logger.error('fail|exception|base exec_r error|%s' % traceback.format_exc())

    def exec_r_one(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except:
            logger.error('fail|exception|base exec_r_one error|%s' % traceback.format_exc())


    def exec_w(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            sid = self.conn.insert_id()
            self.conn.commit()
            return sid
        except:
            self.conn.rollback()
            logger.error('fail|exception|base exec_w error|%s' % traceback.format_exc())

    def close(self):
        self.conn.close()
