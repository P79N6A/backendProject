import json
import os
import re
import traceback

from lib.log import get_logger
from busi.dao.base import BaseDao
from busi.dao.data import Video
from engines.engines import EngineFactory

logger = get_logger('resolver')

class Resolver(object):
    def __init__(self):
        self.rule_dir = 'cfg/rules'
        self.rules = []
        self.cmds  = []

    def valid_rule(self, rule):
        return rule.get('id') and rule.get('key') and rule.get('values')

    def valid_cmd(self, cmd):
        return cmd.get('cmd') and cmd.get('valid')

    def resolve_config(self):
        try:
            files= os.listdir(self.rule_dir)
            for f in files:
                if not os.path.isdir(f):
                    tmp_file = '%s/%s'%(self.rule_dir, f)
                    with open(tmp_file) as data_file:
                        try:
                            config = json.load(data_file)
                        except:
                            logger.error('config file format error, please check:%s'%tmp_file)
                else:
                    continue

                game_id = config['game_id'] if config.has_key('game_id') else 0

                cmds  = config['cmds'] if config.has_key('cmds') else None 
                rules = config['rules'] if config.has_key('rules') else None

                if not (game_id and cmds and rules):
                    logger.warn('[WARNING]rule config file error, please check:%s' % tmp_file)
                    continue

                for rule in rules:
                    if not self.valid_rule(rule):
                        continue
                    obj = {}
                    obj['id']     = '%s_%s'%(f, rule['id'])
                    obj['key']    = rule['key']
                    obj['values'] = rule['values']
                    obj['game_id'] = game_id
                    self.rules.append(obj)

                for item in cmds:
                    if not self.valid_cmd(item):
                        continue
                    obj = {}
                    obj['game_id'] = game_id
                    ops = re.findall(r'[&,|]', item['cmd'])
                    rule_ids = re.split(r'[&,|]', item['cmd'])
                    obj['operator'] = re.findall(r'[&,|]', item['cmd'])
                    obj['rules'] = ['%s_%s'%(f, r) for r in rule_ids]

                    self.cmds.append(obj)

            #filter(lambda item:item['id']==1, lst)
            #self.rules = [{'id':1,'game_id':1007039,'key':'role','values':['HN131']}, {'id':2,'game_id':1007039,'key':'multikill','values':['4k1']}]
            #self.operator = ['&']
        except:
            logger.error(traceback.format_exc())

    def start(self, num=10):
        self.resolve_config()

        if not (len(self.rules) and len(self.cmds)):
            logger.info('rules or cmds is null, return')
            return []

        results = []

        while len(self.cmds):
            cmd      = self.cmds.pop(0)
            rules    = cmd['rules']
            operator = cmd['operator']

            if not (rules and len(rules)):
                logger.info('rules is null, return')
                return []

            engines = []
            weight_num = num * 10
            b = BaseDao()
            dao = Video(b)
            #keys = []
            tmp_rules = rules[:]
            while len(tmp_rules):
                rule_id = tmp_rules.pop(0)
                tmp = filter(lambda item:item['id']==rule_id, self.rules)
                if not (tmp and len(tmp)):
                    continue
                engine_info = tmp[0]
                game_id = engine_info.get('game_id')
                name = engine_info.get('key')
                #keys.append(name)
                values = engine_info.get('values')
                engine = EngineFactory.config(name).produce(game_id=game_id,values=values,dao=dao,video_num=num)
                if not engine:
                    logger.error('engine:%s resolve error, return'% name)
                    return None
                engines.append(engine)


            videos = []
            while 1:
                tmp_engines  = engines[:]
                tmp_operator = operator[:]
                if not len(tmp_engines):
                    logger.info('engine is null, return')
                    return

                pre_engine = tmp_engines.pop(0)
                while len(tmp_engines):
                    next_engine = tmp_engines.pop(0)
                    pre_engine = pre_engine.join(next_engine=next_engine, operator=tmp_operator.pop(0), withouts=videos)

                res = pre_engine.join(withouts=videos)
                if res and len(res):
                    videos.extend(res)
                    if len(videos) >= num:
                        break
                else:
                    break

            results.append({'candidates' : videos, 'cmd' : cmd})
            logger.info('resolve result:%s'%results)

        b.close()
        return results


if __name__ == "__main__":
    resolver = Resolver()
    res = resolver.start()
