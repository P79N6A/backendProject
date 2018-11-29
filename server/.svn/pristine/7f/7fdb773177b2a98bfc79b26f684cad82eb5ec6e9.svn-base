class UserRecommender(object):
    def __init__(self,base=None):
        self.base = base

    def add_recommend(self, user_id, rec_list_str):
        sql = "replace into t_user_recommend(user_id,video_ids) values(%s,%s)"
        self.base.exec_w(sql, user_id, rec_list_str)
