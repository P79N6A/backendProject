# -*- coding: UTF-8 -*-
from lib.log import get_logger

logger = get_logger('db')

class Tag(object):
    def __init__(self, base):
        self.base = base

    def get_tags_by_content(self, content_id = 'unknown'):
        sql = '''
                select SQL_CALC_FOUND_ROWS concat(t2.prefix, t1.idx) as no, t1.name as text
                from dic_tag_data t1 left join dic_tag_name t2 on t1.content_id=t2.content_id and t1.tag_name=t2.tag_name
                where t1.content_id=%s
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql, content_id)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        all_tag      = _Tag()
        all_tag.text = '全部'
        all_tag.no   = 'all'

        data  = []
        data.append(all_tag)
        for row in rows:
            tag = self._convert_row_2_object(row)
            data.append(tag)
        return (total + 1, data)

    def get_all_content(self):
        sql = '''
                select SQL_CALC_FOUND_ROWS content_id as no, content_name as text
                from t_content
                where status=1
                order by ord
        '''
        total_sql = "select FOUND_ROWS() as total"

        rows      = self.base.exec_r(sql)
        total_row = self.base.exec_r(total_sql)

        total = 0
        if (len(total_row) > 0):
            total = total_row[0]['total']

        all_tag      = _Tag()
        all_tag.text = '全部'
        all_tag.no   = 'all'

        data  = []
        data.append(all_tag)
        for row in rows:
            tag = self._convert_row_2_object(row)
            data.append(tag)
        return (total + 1, data)

    def _convert_row_2_object(self, row):
        obj      = _Tag()
        obj.no   = row['no']
        obj.text = row['text']
        return obj

class _Tag(object):
    def __init__(self, text = '', no = ''):
        self.text = text
        self.no   = no

    def toDict(self):
        dic         = {}
        dic['text'] = self.text
        dic['id']   = self.no
        return dic

