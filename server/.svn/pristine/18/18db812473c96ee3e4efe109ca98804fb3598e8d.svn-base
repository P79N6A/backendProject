import sys
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/third_res')

from common.tool import sha_bin as func_sha_bin
from common.tool import sha_str as func_sha_str
from common.tool import md5_str as func_md5_str
from common.tool import tobytes
from lib.log import get_logger
from acloud.net.http_api import upload_file_to_http_svr
from acloud.net.http_api import fileUserApplyUpload
from acloud.m_struct.define import UPLOADFILE_SUCCESS

logger = get_logger('acloud')

class Uploader(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.block_size = 512*1024


    def upload(self, server='', port=0, hex_dirkey='', sha_bin='', fsize=0):
        if not (self.file_path and len(self.file_path) >= 0):
            logger.info('file path:%s invalid, return' % self.file_path)
            return False

        if not (server and port and hex_dirkey and sha_bin):
            logger.info('args invalid, return')
            return False

        fd = open(self.file_path, 'r')
        flag = 0
        offset = 0
        next_offset = 0
        #print 'upload file size:',fsize

        while offset != fsize and (not flag):
            fd.seek(offset)
            buf = fd.read(self.block_size)
            count = 10
            while not flag:
                next_offset,flag,ret = upload_file_to_http_svr(server,port,sha_bin,hex_dirkey,fsize,buf,offset,flag)
                #print 'next_offset:%s,flag:%s,ret:%s' % (next_offset,flag,ret)
                count -= 1
                if count == 0:
                    print 'no chance,close'
                    fd.close()
                    return False
                if next_offset == 0 and flag == 0:
                    print 'continue...'
                    continue
                if ret == UPLOADFILE_SUCCESS:
                    #print 'offset upload success,next_offset',next_offset
                    offset = next_offset
                    break

        fd.close()
        return True


    def upload_self(self, **args):
        if not (self.file_path and len(self.file_path) >= 0):
            logger.info('file path:%s invalid, return' % self.file_path)
            return

        sha_str = func_sha_str(self.file_path)
        md5_str = func_md5_str(self.file_path)
        sha_bin = func_sha_bin(self.file_path)

        serverName  = args['serverName']
        fileid      = args['fileid']
        fsize       = args['fsize']
        filetype    = args['filetype']
        uin         = args['uin']
        uip         = args['uip']
        otype       = args['otype']
        bizid       = args['bizid']
        addrtype    = args['addrtype']
        resp = fileUserApplyUpload(serverName,fileid,fsize,filetype,uin,uip,otype,bizid,addrtype,sha_str,md5_str)
        if not resp:
            print 'fileUserApplyUpload error'
            return

        hex_dirkey = resp['checkkey']
        port       = resp['port']
        server     = resp['server']
        #print port,server
        fd = open(self.file_path, 'r')
        flag = 0
        offset = 0
        next_offset = 0
        #print 'upload file size:',fsize

        while offset != fsize and (not flag):
            fd.seek(offset)
            buf = fd.read(self.block_size)
            count = 10
            while not flag:
                next_offset,flag,ret = upload_file_to_http_svr(server,port,sha_bin,hex_dirkey,fsize,buf,offset,flag)
                #print 'next_offset:%s,flag:%s,ret:%s' % (next_offset,flag,ret)
                count -= 1
                if count == 0:
                    print 'no chance,close'
                    fd.close()
                    return False
                if next_offset == 0 and flag == 0:
                    print 'continue...'
                    continue
                if ret == UPLOADFILE_SUCCESS:
                    #print 'offset upload success,next_offset',next_offset
                    offset = next_offset
                    break

        fd.close()
        return True


if __name__ == "__main__":
    #args = ('10.137.134.215','1010_11145678901234567890123456755555',28075473,'mp4',770125953,'10.177.140.24','json',1010,2,'e77c13a485853b3e68168e4a9095c4fa020d3f4f','1db83ae8ecc37361a698d46bd8ebba6b')
    import os
    file_path = '/Users/shawn/Downloads/yx43.mp4'
    args = {}
    args['serverName'] = '10.137.134.215'
    args['fileid']     = '1010_11145678901234567890123456755555'
    args['fsize']      = os.stat(file_path).st_size
    args['filetype']   = 'mp4'
    args['uin']        = 770125953
    args['uip']        = '10.177.140.24'
    args['otype']      = 'json'
    args['bizid']      = 1010
    args['addrtype']   = 2
    uploader = Uploader(file_path)
    uploader.upload(**args)
