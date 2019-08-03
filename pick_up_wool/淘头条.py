# -*- coding: utf-8 -*-

__author__ = 'Jim'

import random

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import datetime

poco = AndroidUiautomationPoco()


def init():
    global poco
    poco = AndroidUiautomationPoco()


def backup_keyevent():
    keyevent("BACK")


def next_page():
    print("下一页")
    start_point = round(random.uniform(0.2, 0.6), 2)
    end_point = round(random.uniform(0.7, 0.9), 2)
    duration = round(random.uniform(0.5, 0.8), 2)
    poco.swipe([start_point, end_point], [start_point, end_point - 0.7], duration=duration)


def swipe_news():
    start_point = random.uniform(0.6, 0.9)
    end_point = random.uniform(0.9, 0.7)
    duration = round(random.uniform(4, 5), 2)
    poco.swipe([start_point, end_point], [start_point, end_point - 0.6], duration=2)


def see_news_time():
    see_time = round(random.uniform(0.8, 1.5), 2)
    print("see_time = {}".format(see_time))
    time.sleep(see_time)

def next_small_video():
    print("下一个视频")
    x_pos = round(random.uniform(0.5, 0.9), 2)
    y_pos = round(random.uniform(0.85, 0.75), 2)
    duration = round(random.uniform(0.1, 0.2), 2)
    poco.swipe([x_pos, y_pos], [x_pos - 0.05, y_pos - 0.8], duration=duration)


def top_gain_coin():
    """
    时段奖励
    :return:
    """
    top_gain = poco(name="com.ly.taotoutiao:id/tv_time_countdown", text="领取")
    if top_gain.exists():
        print("时段奖励领取")
        top_gain.click()
        time.sleep(3)
        # poco(name="com.ly.taotoutiao:id/btn_close").click()
        poco(name="com.ly.taotoutiao:id/btn_close").wait(3).click()


def watch_news():
    while True:

        news_list = poco("com.ly.taotoutiao:id/mRecyclerView").children()

        for news in news_list:
            news_title = news.offspring("com.ly.taotoutiao:id/tv_topnews_title")
            news_foot = news.offspring("com.ly.taotoutiao:id/tv_topnews_timeandsource")

            if not news_title.exists() or not news_foot.exists():
                print("不是完整的新闻，跳过")
                continue

            # if news.offspring(text="了解详情").exists():
            #     print("广告，跳过")
            #     continue

            # if news.offspring(text="立即下载").exists():
            #     print("下载，跳过")
            #     continue

            #  视频跳过
            # start_video = news.offspring("com.cashtoutiao:id/alivc_player_state")
            # if start_video.exists():
            #     start_video.click()
            #     play_video()
            #     backup_keyevent()
            #     continue

            print("正在看 {}".format(news_title.get_text()))
            news_title.click()

            try:
                play_news()
            except Exception as e:
                print("出现异常 = {}".format(str(e)))
                init()

            backup_keyevent()

            # 顶上时段奖励
            top_gain_coin()

        next_page()


def play_news():
    max_times = random.randint(5, 10)
    now_times = 0

    while True:

        # 打开全文
        click_all = poco(name="展开阅读全文")
        if click_all.exists():
            print("展开全文")
            click_all.click()

        swipe_news()

        see_news_time()

        # 阅读结束
        # if poco("com.cashtoutiao:id/tv_title").exists():
        #     print("遇到广告，文章阅读完毕，退出")
        #     break

        # 超过次数结束
        if now_times == max_times:
            print("超过次数，退出新闻")
            break

        now_times += 1

    print("看完新闻..")


def watch_small_video():

    while True:

        play_small_video()

        next_small_video()


def play_small_video():
    print("开始看小视频")
    start_time = datetime.datetime.now()

    # 是视频最大时间
    max_seconds = random.randint(10, 20)

    while True:

        end_time = datetime.datetime.now()

        if (end_time - start_time).seconds > max_seconds:
            break

    print("看完小视频")


def run():
    watch_news()

    # watch_small_video()


if __name__ == '__main__':
    run()
