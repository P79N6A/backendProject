from tool.factory import Factory

class Engine(object):

    def logic(self, withouts=None):
        raise NotImplementedError

    #xxA.join(next_engine=xxB,operator='&',[]).join(operator='',[])
    def join(self, next_engine=None, operator='', withouts=None):
        pipe_join = self.logic(withouts=withouts)
        if next_engine:
            next_engine.pipe = pipe_join
            next_engine.operator = operator
            return next_engine
        else:
            return pipe_join

    def logic(self, withouts=None):
        if not self.values:
            return self.pipe

        pipe_join = []
        if self.pipe and isinstance(self.pipe, list):

            if self.operator == '&':
                for video_info in self.pipe:
                    tags = video_info.tags
                    intersection = [i for i in tags if i in self.values]
                    if len(intersection):
                        pipe_join.append(video_info)
            elif self.operator == '|':
                tmp_num = 0
                datas = self.dao.get_video_info_by_tags(game_id=self.game_id,tags=self.values,video_num=self.weight_num,withouts=withouts)
                for video_info in datas:
                    pipe_join.append(video_info)
                    tmp_num += 1
                    if tmp_num >= self.video_num:
                        datas.close()
                        break
                pipe_join = list(set(self.pipe).union(set(pipe_join)))
            else:
                logger.info('%s operator is not supported')
                pipe_join = self.pipe

        else:
            tmp_num = 0
            datas = self.dao.get_video_info_by_tags(game_id=self.game_id,tags=self.values, video_num=self.weight_num,withouts=withouts)
            for video_info in datas:
                pipe_join.append(video_info)
                tmp_num += 1
                if tmp_num >= self.video_num:
                    datas.close()
                    break


        return pipe_join

class TagEngine(Engine):

    def __init__(self, game_id='', video_num=100, values='', dao=None):
        self.game_id = game_id
        self.video_num = video_num
        self.operator  = ''
        self.values = values
        self.dao = dao
        self.pipe = None
        self.weight_num = video_num * 10

    def set_tags(self, tags=None):
        self.values = tags


class RoleEngine(Engine):

    def __init__(self, game_id='', video_num=100, values='', dao=None):
        self.game_id = game_id
        self.video_num = video_num
        self.operator  = ''
        self.values = values
        self.dao = dao
        self.pipe = None
        self.weight_num = video_num * 10

    def set_role(self, roles=None):
        self.values = roles



class MultiKillEngine(Engine):

    def __init__(self, game_id='', video_num=10, values='', dao=None):
        self.game_id = game_id
        self.video_num = video_num
        self.operator  = ''
        self.values = values
        self.dao = dao
        self.weight_num = video_num * 10
        self.pipe = None

    def set_multis(self, multis=None):
        self.values = multis

    #def logic(self, withouts=None):
    #    if not self.multis:
    #        return self.pipe

    #    pipe_join = []
    #    if self.pipe and isinstance(self.pipe, list):

    #        if self.operator == '&':
    #            for video_info in self.pipe:
    #                tags = video_info.tags
    #                intersection = [i for i in tags if i in self.multis]
    #                if len(intersection):
    #                    pipe_join.append(video_info)
    #        elif self.operator == '|':
    #            for video_info in self.dao.get_video_info_by_multi_kill(game_id=self.game_id,multis=self.multis, video_num=self.video_num):
    #                pipe_join.append(video_info)
    #            pipe_join = list(set(self.pipe).union(set(pipe_join)))
    #        else:
    #            logger.info('%s operator is not supported')
    #            pipe_join = self.pipe

    #    else:
    #        for video_info in self.dao.get_video_info_by_multi_kill(game_id=self.game_id,multis=self.multis, video_num=self.video_num):
    #            pipe_join.append(video_info)


    #    return pipe_join

class EngineFactory(Factory):
    engine_name = ''

    @classmethod
    def config_base(cls):
        return EngineFactory

    @classmethod
    def config_sub(cls):
        return Engine_Map.get(cls.engine_name)

    @classmethod
    def config(cls, name):
        cls.engine_name = name
        return cls



Engine_Map = {
    'role' : RoleEngine,
    'multikill' : MultiKillEngine,
    'tags'  : TagEngine 
}
