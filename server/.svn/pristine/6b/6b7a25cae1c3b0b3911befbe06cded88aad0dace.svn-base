import traceback

from lib.log import get_logger
from dao.base import BaseDao
from dao.version import Version

logger = get_logger('busi')

class VersionService(object):
    def __init__(self):
        self.__base = None

    def get_update(self, version_code):
        self.__base = BaseDao()
        version     = Version(self.__base)
        versions    = version.get_version(version_code)

        max_version_code = version_code
        download_url     = ''
        force            = 0
        for ver in versions:
            if (ver.version_code > max_version_code):
                download_url     = ver.version_url
                max_version_code = ver.version_code
            if (ver.version_code == version_code and ver.use_flag == 0):
                force = 1
        return (download_url, force)

    def close(self):
        if (self.__base is not None):
            self.__base.close()

