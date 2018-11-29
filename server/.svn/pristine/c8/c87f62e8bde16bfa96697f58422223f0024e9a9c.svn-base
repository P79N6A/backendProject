# -*- coding: UTF-8 -*-

TABLE_MAP = {
    '100001' : 't_dance_music',
    '100002' : 't_dance_music'
}
class Notice(object):
    def __init__(self, base):
        self.base = base

    def get_new_notice(self, timestamp=0):
        import time
        now = int(time.time())
        result = []
        sql  = """
                  select t1.resource_id, t1.create_time, t2.id, t2.type_id, t2.content,
                  t3.id as userid, t3.nickname, t3.user_icon, t3.sex
                  from t_notice_detail t1
                  join (select max(create_time) marg, notice_id from t_notice_detail group by notice_id) temp
                  on t1.create_time=temp.marg and t1.notice_id=temp.notice_id
                  left join dic_notice t2 on t1.notice_id=t2.type_id
                  left join t_open_user_profile t3 on t1.user_id=t3.id
                  where t1.expired>%s and t1.create_time>%s
               """
        rows = self.base.exec_r(sql, now, timestamp)

        for row in rows:
            notice_obj = self._convert_object(row)
            res_id     = notice_obj.res_id
            table_name = TABLE_MAP[str(notice_obj.type_id)]
            if res_id and table_name:
                sql = """
                        select pic_url, name, player from {0} where id=%s
                """.format(table_name)
                rows = self.base.exec_r(sql, res_id)
                if rows and len(rows):
                    row = rows[0]
                    notice_obj.profile['pic_url'] = row.get('pic_url') or ''
                    notice_obj.profile['name']    = row.get('name') or ''
                    notice_obj.profile['player']  = row.get('player') or ''

            result.append(notice_obj)

        return result


    def _convert_object(self, row):
        notice             = _Notice()
        notice.id          = row.get('id') or 0
        notice.res_id      = row.get('resource_id') or 0
        notice.type_id     = row.get('type_id') or 0
        notice.content     = row.get('content') or ''
        notice.userid      = row.get('userid') or 0
        notice.nickname    = row.get('nickname') or ''
        notice.user_icon   = row.get('user_icon') or ''
        notice.sex         = row.get('sex') or 0
        notice.create_time = row.get('create_time') or 0
        return notice

class _Notice(object):
    def __init__(self):
        self.id          = 0
        self.res_id      = 0
        self.type_id     = 0
        self.content     = ''
        self.userid      = 0
        self.nickname    = ''
        self.user_icon   = ''
        self.sex         = 0
        self.create_time = 0
        self.profile     = {}

    def toDict(self):
        dic = {}
        dic['id']           = self.id
        dic['type_id']      = self.type_id
        dic['content']      = self.content
        dic['userid']       = self.userid
        dic['nickname']     = self.nickname
        dic['user_icon']    = self.user_icon
        dic['sex']          = self.sex
        dic['create_time']  = self.create_time
        dic['profile']      = self.profile

        return dic
