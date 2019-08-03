# -*- coding: utf-8 -*-

__author__ = 'Jim'

import datetime
import random

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

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
    poco.swipe([start_point, end_point], [start_point, end_point - 0.6], duration=duration)


def swipe_news():
    start_point = random.uniform(0.6, 0.9)
    end_point = random.uniform(0.9, 0.7)
    duration = round(random.uniform(4, 5), 2)
    poco.swipe([start_point, end_point], [start_point, end_point - 0.6], duration=2)


def see_news_time():
    see_time = round(random.uniform(0.8, 1.5), 2)
    print("see_time = {}".format(see_time))
    time.sleep(see_time)


def top_gain_coin():
    """
    时段奖励
    :return:
    """
    top_gain = poco(name="com.cashtoutiao:id/count_down_tv", text="点击领取")
    if top_gain.exists():
        print("时段奖励领取")
        top_gain.click()
        time.sleep(2)
        poco(name="com.cashtoutiao:id/tv_left", text="忽略").click()


def watch_news():
    while True:

        news_list = poco("android:id/list").children()

        for news in news_list:
            news_title = news.offspring("com.cashtoutiao:id/tv_title")
            news_foot = news.offspring("com.cashtoutiao:id/tv_src")

            if not news_title.exists() or not news_foot.exists():
                print("不是完整的新闻，跳过")
                continue

            if news.offspring(text="了解详情").exists():
                print("广告，跳过")
                continue

            if news.offspring(text="立即下载").exists():
                print("下载，跳过")
                continue

            #  视频跳过
            start_video = news.offspring("com.cashtoutiao:id/alivc_player_state")
            if start_video.exists():
                print("视频跳过")
                # start_video.click()
                # play_video()
                # backup_keyevent()
                continue

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
        swipe_news()

        # 打开全文
        # click_all = poco("com.cashtoutiao:id/root_nested_scroll").offspring(touchable=True)
        click_all = poco("展开全文", touchable=True)
        if click_all.exists():
            click_all.click()

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


def play_video():
    print("开始看视频")
    start_time = datetime.datetime.now()
    watch_time = random.randint(30, 50)

    while True:

        # 出现重播，已经播放完，退出视频
        if poco("com.cashtoutiao:id/alivc_player_retry").exists():
            break

        end_time = datetime.datetime.now()

        # 播放到一定时间就退出视频
        if (end_time - start_time).seconds > watch_time:
            print("播放时间超时， 需要退出视频")
            break

    print("看完视频了..")


def run():
    watch_news()


if __name__ == '__main__':
    run()
