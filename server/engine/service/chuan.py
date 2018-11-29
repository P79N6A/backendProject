import traceback
import thread

from busi.dao.base import BaseDao
from busi.dao.data import Video
from busi.dao.data import Chuan
from multiprocessing import Process
from lib.log import get_logger

logger = get_logger('main')

class ChuanService(object):
 
    def __init__(self, base=None):
        self.b = base or BaseDao()
        self.chuan_dao = Chuan(self.b)
        self.video_dao = Video(self.b)

    def close(self):
        if self.b:
            self.b.close()
            self.b = None

    def get_urls(self, vids, video_infos):
        from lib.config import read_l5_info
        from l5.get_router import get_router
        from transport.client import UDPClient
        from adjuster.adjuster_tool import get_download_url_and_definition
        modid,cmdid = read_l5_info()
        host,port = get_router(modid, cmdid)
        udp_client = UDPClient(host, port)
        tmp = []
        if video_infos and len(video_infos) and vids and len(vids):
            for vid in vids:
                filters = filter(lambda o:o.video_id == vid, video_infos)
                if not len(filters):
                    continue
                item    = filters[0]
                vid     = item.video_id
                game_id = item.game_id
                if not (vid and game_id):
                    logger.warn("vid:%s or game_id:%s is null, skip.."%(vid, game_id))
                    continue
                url,definition = get_download_url_and_definition(vid.encode('utf8'), int(game_id), udp_client=udp_client)
                if url:
                    item.url = url
                    item.definition = definition
                    logger.info('get download url:%s of vid:%s, game_id:%s'%(url, vid, game_id))
                    tmp.append(item)
                else:
                    logger.warn("vid:%s game_id:%s get download url is null, skip.."% (vid, game_id))

        return tmp

    def createJob(self, uid='', vids=[], title=''):
        data = {'jobid' : -1}
        if not (uid and vids and len(vids)):
            logger.error('uid:%s or vids:%s is null'%(uid, vids))
            raise Exception('uid:%s or vids:%s is null'%(uid, vids))

        jid = self.chuan_dao.createJob(uid=uid, vids=vids)
        video_infos = self.video_dao.get_videoInfo_by_vids(vids=vids)
        game_id = 0
        for item in video_infos:
            if item.video_id == vids[0]:
                game_id = item.game_id
                break

        video_infos = self.get_urls(vids, video_infos)
        if not (video_infos and len(video_infos)):
            logger.error('video info is null,vids:%s'% vids)
            raise Exception('video info is null,vids:%s'% vids)

        userinfo = self.chuan_dao.get_userinfo_by_uid(uid)
        if not userinfo:
            logger.error('user info is null,uid:%s'% uid)
            raise Exception('user info is null,uid:%s'% uid)
        #p = Process(target=self.work, args=(video_infos, jid,))
        #p.start()
        #self.work(video_infos, jid)
        thread.start_new_thread(self.work, (video_infos, jid, title, userinfo, int(game_id),))
        data['jobid'] = jid
        logger.info('jid:%s start..'% jid)

        return data

    def queryJob(self, jid=None):
        data = {'jobid' : jid, 'status': -1, 'vid':''}
        if jid is None:
            logger.error('jid:%s is null'%(jid))
            raise Exception('jid:%s is null'%(jid))

        status,vid     = self.chuan_dao.query_chuan_status(jid=jid)

        data['status'] = status
        data['vid']    = vid

        return data

    def queryDoingJob(self, uid=None):
        data = {'jobids' : [] }
        if uid is None:
            logger.error('uid:%s is null'%(uid))
            raise Exception('uid:%s is null'%(uid))

        for vid in self.chuan_dao.query_chuan_doing_jobs(uid=uid):
            data['jobids'].append(vid)

        return data


    def work(self, video_infos, jid, title, userinfo, game_id):
        b =  BaseDao()
        try:
            self.chuan_dao = Chuan(b)
            succ, vid = self._merge_and_up(video_infos, jid, b, title, userinfo, game_id)
            if succ:
                self.chuan_dao.update_chuan_status(jid=jid, status=1, vid=vid)
            else:
                self.chuan_dao.update_chuan_status(jid=jid, status=-1)
        except:
            logger.error( traceback.format_exc() )
        finally:
            if b:
                b.close()

    def _merge_and_up(self, video_infos, jid, b, title, userinfo, game_id):
        from video_processor.processor import VideoProcessor
        from uploader.uploader import Uploader
        from lib.config import read_l5_info
        from l5.get_router import get_router
        from transport.client import UDPClient
        from busi.dao.common import assemble
        from busi.dao.common import valid
        vid = ''
        fail_res = (False, vid)
        succ_res = (True, vid)
        if not (video_infos and len(video_infos)):
            logger.error('video infos is null, jid:%s fail.'% jid)
            return fail_res
        try:
            processor = VideoProcessor()
            modid,cmdid = read_l5_info()
            host,port = get_router(modid, cmdid)
            if not (host and port):
                logger.error('l5 get error')
                return
            merge_info  = processor.work(video_infos)
            file_path = merge_info.get('file_path')
            workspace   = merge_info.get('workspace')
            if not (merge_info and file_path):
                logger.error('merge fail, jid:%s fail.'% jid)
                return fail_res

            udp_client = UDPClient(host=host, port=port)
            up = Uploader(file_path, 'mp4', udp_client)
            up_info = up.upload(addrtype=2, game_id=game_id)
            #up_info = up.upload(addrtype=2)
            if workspace:
                import shutil
                logger.info('delete workspace:%s'%workspace)
                shutil.rmtree(workspace)

            if up_info['status'] != 0:
                logger.error('upload merge_file fail, jid:%s fail.'%jid)
                return fail_res 

            vid = up_info['vid']
            if not vid:
                logger.error('upload merge_file fail, jid:%s fail.'%jid)
                return fail_res

            assemble_obj = assemble(video_infos, up_info, udp_client)
            if assemble_obj and valid(assemble_obj):
                #assemble_obj['nickname'] = userinfo[0]
                assemble_obj['uid']      = userinfo[1]
                assemble_obj['title'] = title or assemble_obj['title']
                self.video_dao = Video(b)

                #print assemble_obj
                self.video_dao.add_item(assemble_obj)
                self.video_dao.add_video_game(vid, game_id)
                #self.chuan_dao.update_chuan_status(jid=jid, status=1, vid=vid)
            else:
                logger.info('jid:%s assemble fail.'%jid)
                return fail_res

            logger.info('jid:%s finish success.'%jid)
            succ_res = (True, vid)
            return succ_res
        except:
            logger.error(traceback.format_exc())
            return fail_res
