from busi.dao.base import BaseDao
from busi.dao.data import Video

def get_second_c_by_gameid(self, game_id=0):
    b = BaseDao()
    video_dao = Video(b)
    name = video_dao.get_content_by_game_id(game_id)
    b.close()

    return name
