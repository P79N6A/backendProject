# -*- coding: UTF-8 -*-

class Category(object):
    def __init__(self, base):
        self.base = base

    def get_all_category(self):
        sql  = "select name, icon, type, content_id from t_categorys where status=1 order by f_order"
        rows = self.base.exec_r(sql)

        result = []
        for row in rows:
            category = self._convert_object(row)
            result.append(category)
        return result

    def _convert_object(self, row):
        category         = _Category()
        category.name    = row['name']
        category.icon    = row['icon']
        category.c_type  = row['type']
        category.type_id = row['content_id']
        return category

class _Category(object):
    def __init__(self, name = '', icon = '', c_type = '', type_id = ''):
        self.name    = name
        self.icon    = icon
        self.c_type  = c_type
        self.type_id = type_id

    def toDict(self):
        dic = {}
        dic['name']    = self.name
        dic['icon']    = self.icon
        dic['c_type']  = self.c_type
        dic['type_id'] = self.type_id
        return dic

