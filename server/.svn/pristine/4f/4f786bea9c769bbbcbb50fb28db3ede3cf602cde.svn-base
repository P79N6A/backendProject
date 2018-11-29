# -*- coding: UTF-8 -*-
import schedule
import time
from lib.recommender import Recommender
def recommend_video():
    rec = Recommender(num=50)
    rec.recommend()
    rec.close()

def recommend_music():
    rec = Recommender()
    rec.music_recommend()
    rec.close()


if __name__ == "__main__":
    schedule.every().hour.do(recommend_music)
    schedule.every(30).minutes.do(recommend_video)
    while True:
        schedule.run_pending()
        time.sleep(10)
