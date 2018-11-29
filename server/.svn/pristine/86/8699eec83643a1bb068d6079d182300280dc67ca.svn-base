# -*- coding: UTF-8 -*-

class Application(object):
    def __init__(self, base):
        self.base = base

    def get_all_app(self):
        sql  = "select content_id, content_name, icon_url from t_content where status=1"
        rows = self.base.exec_r(sql)

        result = []
        for row in rows:
            app = self._convert_object(row)
            result.append(app)
        return result

    def _convert_object(self, row):
        app              = _Application()
        app.content_id   = row['content_id']
        app.content_name = row['content_name']
        app.icon_url     = row['icon_url']
        return app

class _Application(object):
    def __init__(self, content_id = '', app_name = '', icon_url = ''):
        self.content_id   = content_id
        self.content_name = content_name
        self.icon_url     = icon_url

    def toDict(self):
        dic = {}
        dic['app_name'] = self.content_name
        dic['app_icon'] = self.icon_url
        return dic

