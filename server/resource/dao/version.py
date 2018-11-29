from lib.log import get_logger

class Version(object):
    def __init__(self, base):
        self.base   = base
        self.logger = get_logger('db')

    def get_version(self, version_code):
        sql = """
                select id,version_code,version_name,use_flag,version_url,create_time,create_user,modify_time,modify_user
                from t_version where status=1 and version_code>=%s
            """

        result = []
        for val in self.base.exec_r(sql, version_code):
            version              = _Version()
            version.f_id         = val['id']
            version.version_code = val['version_code']
            version.version_name = val['version_name']
            version.use_flag     = val['use_flag']
            version.version_url  = val['version_url']
            version.create_time  = val['create_time']
            version.create_user  = val['create_user']
            version.modify_time  = val['modify_time']
            version.modify_user  = val['modify_user']
            result.append(version)
        return result


class _Version(object):
    def __init__(self, f_id = 0, version_code = 0, version_name = '', use_flag = 0, version_url = 0,
            create_time = '', create_user = 0, modify_time = '', modify_user = ''):
        self.f_id         = f_id
        self.version_code = version_code
        self.version_name = version_name
        self.use_flag     = use_flag
        self.version_url  = version_url
        self.create_time  = create_time
        self.create_user  = create_user
        self.modify_time  = modify_time
        self.modify_user  = modify_user

