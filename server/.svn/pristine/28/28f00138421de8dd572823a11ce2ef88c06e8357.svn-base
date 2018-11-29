# -*- coding: UTF-8 -*-
import MySQLdb
from lib.config import read_db_config

class BaseDao(object):
    def __init__(self, conf=read_db_config()):
        self.conn = MySQLdb.connect(**conf)
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def exec_r(self, sql, *args):
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchall()
        except Exception as err:
            raise err

    def exec_r_one(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as err:
            raise err


    def exec_w(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            sid = self.conn.insert_id()
            self.conn.commit()
            return sid
        except Exception as err:
            self.conn.rollback()
            raise err

    def close(self):
        self.conn.close()
