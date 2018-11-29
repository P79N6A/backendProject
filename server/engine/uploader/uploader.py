import sys
import os
import traceback
sys.path.append('/Users/shawn/tencent/src/newbridge_proj/trunk/server/engine')
from hero.qt_herlper import QtHelper
import hero.proto.hero_time_pb2 as pb_hero
from lib.config import read_l5_info
from lib.log import get_logger
from acloud.upload import Uploader as aUploader
from common.tool import sha_bin as func_sha_bin
from common.tool import sha_str as func_sha_str
from common.tool import md5_str as func_md5_str


logger = get_logger('uploader')


class Uploader(object):
    def __init__(self, file_path, file_type, udp_client):
        self.file_path = file_path
        self.file_type = file_type
        self.udp_client = udp_client
        self.uiAppid    = 211


    def apply_uploader_req(self, vid=0, filetype='', filesize=0, filesha='', filemd5='',
                           addrtype=2, game_id=0, uin=289296918):
        try:
            qt = QtHelper()
            sess = qt.createSessInfo(pb_hero.CMD_HEROTIMESVR,
                                     pb_hero.SUBCMD_APPLY_UPLOAD_VIDEO,
                                     self.uiAppid, uin)
    
            req = pb_hero.ApplyUploadVideoReq()
            req.file_uuid = vid
            req.filetype  = filetype
            req.filesize  = filesize
            req.filesha   = filesha
            req.filemd5   = filemd5
            req.game_id   = game_id
            req.addrtype  = addrtype
    
    
            res = qt.buildSendPkg(sess, req)
            #b = res.serialize()
    
            self.udp_client.sendData(buf=res.serialize())
            bb = self.udp_client.recvData()
    
            resp = qt.parseReceivePkg(bb)
            resp.unserialize()
            resp_str = str(buffer(resp.body_str)[:])
            pb_resp = pb_hero.ApplyUploadVideoRsp()
            pb_resp.ParseFromString(resp_str)

            return pb_resp
        except:
            logger.error('get error:%s'%traceback.format_exc())

    def upload(self, addrtype=2, game_id=0, uin=289296918):
        up_info = {'game_id':game_id, 'status':0}
        try:
            sha_str = func_sha_str(self.file_path)
            md5_str = func_md5_str(self.file_path)
            sha_bin = func_sha_bin(self.file_path)
            vid      = md5_str
            filesize = os.stat(self.file_path).st_size
            filetype = 'mp4'
            up_info['vid'] = vid

            resp = self.apply_uploader_req(vid=vid,filetype=filetype,filesize=filesize,filesha=sha_str,filemd5=md5_str,
                                           addrtype=addrtype,game_id=game_id,uin=uin)
            if not resp or resp.result:
                logger.warn('upload fail:%s'%resp.error_msg if resp else 'resp is null')
                up_info['status'] = -1
                return up_info
            ip    = resp.svr_ip
            port  = resp.svr_port
            upkey = resp.upload_key
            aUp   = aUploader(self.file_path)
            if not aUp.upload(server=ip, port=port, hex_dirkey=upkey, sha_bin=sha_bin, fsize=filesize):
                up_info['status'] = -1
        except:
            logger.error('upload get error:%s'%traceback.format_exc())
            up_info['status'] = -1
        finally:
            return up_info


if __name__ == "__main__":
    from l5.get_router import get_router
    from transport.client import UDPClient
    import os
    modid,cmdid = read_l5_info()
    host,port = get_router(modid, cmdid)
    if not (host and port):
        logger.error('l5 get error')
        sys.exit(1)
    udp_client = UDPClient(host=host, port=port)
    file_path = '/Users/shawn/Downloads/yx43.mp4'
    uploader = Uploader(file_path,'mp4',udp_client)

    res = uploader.upload(addrtype=2, game_id=1007039)
    udp_client.close()

