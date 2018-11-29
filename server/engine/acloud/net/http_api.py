import httplib
import traceback
import ctypes
import threading
import os
import json
import sys
import socket
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/third_res')

from common.tool import tobytes
from acloud.m_struct.header import StHeader
from acloud.m_struct.header import C_e
from acloud.m_struct.body import StUploadBody
from acloud.m_struct.define import *
from acloud.m_struct.http_conn import getReq
from acloud.m_struct.http_conn import getResp

def _url_open(conn, func, path, body, header):
    try:
        #POST
        #conn_obj.request("POST", "/func","param=0", {"Connection":"Keep-Alive"})
        conn.request(func, path, body, header)
        response = conn.getresponse()
        #return response.read()
        return response
    except:
        print traceback.format_exc()

def fileUserApplyUpload(serverName,fileid,fileSize,filetype,uin,uip,otype,bizid,addrtype,filesha,md5):
    server  = 0
    port    = 0
    checkkey = 0
    conn = httplib.HTTPConnection(serverName, HTTPSVRPORT)
    path = '/applyupload?fileid=%s&filetype=%s&uip=%s&uin=%s&otype=%s&bizid=%s&addrtype=%d&filesize=%ld&filesha=%s&filemd5=%s'\
            % (fileid,filetype,uip,uin,otype,bizid,addrtype,fileSize,filesha,md5)
    #print path
    resp = _url_open(conn, 'GET', path, '',
                    {"Host":serverName})
    if not resp:
        print 'http resp is null'
        return next_offset,flag,UPLOADFILE_RECV_ERR
    resp_obj = json.loads(resp.read())
    conn.close()
    return resp_obj

def upload_file_to_http_svr(server,port,hex_sha,hex_dirkey,fsize,buf,offset,
                           flag):
    #print '@upload to server:%s,port%s'%(server,port)
    conn = httplib.HTTPConnection(server, port)
    try:
        #stHeader
        stHeader = StHeader()
        stHeader.c_e.cmd = socket.htonl(FTN_HTTP_CMD_UPLOAD_SUPER4G_FILE)
        stHeader.magic_num = socket.htonl(FTN_HTTP_MAGIC_NUM)
        stHeader.body_len = socket.htonl(ctypes.sizeof(StUploadBody) + len(buf))
        #print '@@@body len', socket.htonl(ctypes.sizeof(StUploadBody) +
        #                                  len(buf))
        #stHeader.body_len = ctypes.sizeof(StUploadBody) + len(buf)
        stHeader.reserved = socket.htonl(os.getpid() +
                                         threading.current_thread().ident)
        #fd = open('test.header','wb')
        #fd.write(stHeader)
        #fd.close()

        #stBody
        stUploadBody = StUploadBody()
        stUploadBody.file_key_len = 20
        #print '@@@hex_sha', repr(hex_sha)
        stUploadBody.file_key     = tobytes(hex_sha, 20)
        stUploadBody.ukey_len     = FTN_UPLOAD_KEY_LEN
        #print '@@@ukey_len',repr(stUploadBody.ukey_len)
        #print '@@ukey', hex_dirkey
        stUploadBody.ukey         = tobytes(hex_dirkey.decode('hex'), 304)
        stUploadBody.file_sizeH   = fsize >> 32
        stUploadBody.file_size    = fsize & 0xFFFFFFFF
        stUploadBody.offsetH      = offset>>32
        stUploadBody.offset       = offset & 0xFFFFFFFF
        #print '@@@data_len',len(buf)
        stUploadBody.data_len     = len(buf)
        
        content_length = ctypes.sizeof(stHeader) + ctypes.sizeof(stUploadBody) + len(buf)
        #print '@@@content_length', content_length
        data = getReq(stHeader, stUploadBody, buf)


        resp = _url_open(conn, 'POST', '/ftn_handler', data.serialize(),
                        {"Content-Length":content_length})
        if not resp:
            print 'http resp is null'
            return 0,flag,UPLOADFILE_RECV_ERR
        next_offsetL,next_offsetH,flag,code = parseRecvBuf(resp)

        next_offset = (next_offsetH<<32) + next_offsetL
        #print '%s<<32 + %s=%s'%(next_offsetH,next_offsetL,next_offset)
        if code == 200:
            return next_offset,flag,UPLOADFILE_SUCCESS
        else:
            return next_offset,flag,code

    except:
        print '@@@@'
        print traceback.format_exc()
    conn.close()

def parseRecvBuf(resp):
    flag = 0
    next_offset  = 0
    next_offsetH = 0
    code = resp.status or 0
    if code != 200:
        #print resp.status
        code = stresp.stheader.c_e.error
        print 'err'
        print 'stHeader error:',code
        return next_offset,next_offsetH,flag,code

    buf = resp.read()
    stresp = getResp(buf)
    stresp.unserialize()
    stHeader = stresp.stheader
    httpRsp = stresp.sthttpRsp
    if httpRsp:
        print httpRsp.next_offset
        #print httpRsp.next_offsetH
        next_offset  = httpRsp.next_offset
        next_offsetH = httpRsp.next_offsetH
        flag = httpRsp.flag
    else:
        print 'err: httpRsp is null'

    
    return next_offset,next_offsetH,flag,code


def foo(*args):
    return fileUserApplyUpload(*args)

if __name__ == "__main__":
    #conn = httplib.HTTPConnection("www.baidu.com", 80)
    #resp = _url_open(conn, 'GET', '/', 'test', {"Connection":"Keep-Alive"})
    #print resp.status
    #print resp.getheaders()
    #print resp.read()
    #conn.close()


    #(serverName,fileid,fileSize,filetype,uin,uip,otype,bizid,addrtype,filesha,md5)
    args = ('10.137.134.215','1010_11145678901234567890123456755555',28075473,'mp4',770125953,'10.177.140.24','json',1010,2,'e77c13a485853b3e68168e4a9095c4fa020d3f4f','1db83ae8ecc37361a698d46bd8ebba6b')
    #resp = fileUserApplyUpload(*args)
    resp = foo(*args)
    #print resp['checkkey']
