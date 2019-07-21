# -*- coding: utf-8 -*-

"""
东方头条自动化脚本

暂仅支持单设备运行

TODO(Jim): 支持多台设备运行
"""

__author__ = 'Jim'

import datetime
import random
import traceback

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


# from utils.airtest_utils import backup_keyevent

def backup_keyevent():
    keyevent("BACK")


class EastNews(object):
    """
    东方头条的自动化薅羊毛
    """

    def __init__(self):
        self.package_name = "com.songheng.eastnews"
        self.conn()

    def conn(self):
        self.poco = AndroidUiautomationPoco()

    def run(self):

        home()
        start_app(self.package_name)

        self.__pre_skip_ads()
        print("进入主页")

        # 获取顶部的金币
        self.get_top_title_coin()

        self.normal_task()

    def __pre_skip_ads(self):
        """ 预加载，跳过广告，进入主页
        1. 等待广告出现
        2. 点击跳过广告
        3. 等待首页元素加载完成
        :return:
        """

        # 有广告则点击跳过
        ads_element = self.poco(name='android.widget.TextView', text='跳过').wait(10).click()

        # 等待主页显示
        self.poco('com.songheng.eastnews:id/fu').wait_for_appearance(120)

    def get_top_title_coin(self):
        """
        获取顶部金币
        :return:
        """

        top_coin = self.poco(name="com.songheng.eastnews:id/arc", text="领取")
        if top_coin.exists():
            print("点击领取金币")
            top_coin.click()

            # 关闭广告
            self.poco(name="com.songheng.eastnews:id/go").click()
        else:
            print("时间不足或者不在首页")

    def normal_task(self):
        """
        日常任务

        1. 签到
        2. 大转盘
        :return:
        """
        pass

    def watch_news(self):
        """
        看新闻
        :return:
        """

        while True:
            news_list = self.poco("com.songheng.eastnews:id/fu").children()

            for news in news_list:
                news_title = news.offspring("com.songheng.eastnews:id/ot")
                news_foot = news.offspring("com.songheng.eastnews:id/abl")

                # 必须是完整的一条内容才打开，否则跳过
                if not news_title.exists() or not news_foot.exists():
                    print("内容不完整..切换下一条新闻")
                    continue

                # 如果是小视频，跳过
                if news.offspring("com.songheng.eastnews:id/a7a").exists():
                    # print("小视频，跳过")
                    self.play_small_video()
                    backup_keyevent()
                    continue

                # 广告跳过
                if news.offspring("com.songheng.eastnews:id/a5i").exists():
                    print("广告，跳过")
                    continue

                # 下载软件的广告，跳过
                if news.offspring("com.songheng.eastnews:id/zl").exists():
                    print("下载广告，跳过")
                    continue

                if news.offspring("com.songheng.eastnews:id/a4n").exists():
                    self.play_video()
                    backup_keyevent()
                    continue

                print("正在看 {}".format(news_title.get_text()))

                news_title.click()

                try:
                    self.play_news()
                except Exception as e:
                    print("读取新闻时出现异常 = {}".format(str(e)))
                    self.conn()
                    exit(-1)

                print("返回")
                backup_keyevent()

            self.next_page()

    def play_news(self):
        max_times = random.randint(5, 15)
        now_times = 0

        while True:

            start_point = random.uniform(0.6, 0.9)
            end_point = random.uniform(0.9, 0.7)
            duration = round(random.uniform(4, 5), 2)
            self.poco.swipe([start_point, end_point], [start_point, end_point - 0.6], duration=2)

            # 点击查看全文
            click_all = self.poco("点击查看全文")
            if click_all.exists():
                click_all.click()

            # 如果遇到广告, 说明该文章已经读完，可以退出来了
            if self.poco("相关推荐 ").exists():
                break

            # 看会儿新闻
            see_time = round(random.uniform(0.8, 1.5), 2)
            print("see_time = {}".format(see_time))
            time.sleep(see_time)

            # 下滑次数超过最大次数，则退出该新闻
            if now_times == max_times:
                print("超过次数，退出新闻")
                break
            now_times += 1

        print("看完这篇新闻")

    def watch_video(self):
        """
        看视频
        :return:
        """

        # self.poco(name="com.songheng.eastnews:id/js", text="视频").click()

        while True:
            video_elements = self.poco(name="com.songheng.eastnews:id/a0z").children()
            for video_element in video_elements:

                # 如果是广告则跳过
                if video_element.offspring("com.songheng.eastnews:id/a_g").exists():
                    print("视频右下角广告跳过")
                    continue

                # 如果没有标题，则跳过
                video_text = video_element.offspring("com.songheng.eastnews:id/ot")
                video_content = video_element.offspring("com.songheng.eastnews:id/a4d")
                if not video_text.exists() or not video_content.exists():
                    print("标题或者正文视频至少有一个不存在")
                    continue

                print("正在看 {}".format(video_text.get_text()))

                # 打开视频
                video_content.click()

                try:
                    self.play_video()
                except Exception as e:
                    print("出异常 = {}".format(traceback.format_exc()))
                    self.conn()
                    continue

                print("返回")
                backup_keyevent()

            self.close_push_news()
            self.next_page()

    def play_video(self):
        """
        开始播放视频
        :return:
        """

        print("开始看视频")
        start_time = datetime.datetime.now()
        watch_time = random.randint(30, 50)

        while True:

            # 出现重播，已经播放完，退出视频
            if self.poco("com.songheng.eastnews:id/aqh").exists():
                break

            end_time = datetime.datetime.now()

            # 播放到一定时间就退出视频
            if (end_time - start_time).seconds > watch_time:
                print("播放时间超时， 需要退出视频")
                break

            # 看视频的过程中，关闭推送的新闻
            self.close_push_news()

        print("看完视频了..")

    def play_small_video(self):

        print("开始看小视频")
        start_time = datetime.datetime.now()

        # 是视频最大时间
        max_seconds = random.randint(10, 20)

        while True:

            end_time = datetime.datetime.now()

            if (end_time - start_time).seconds > max_seconds:
                break

        print("看完小视频")

    def next_page(self):

        print("下一页")
        start_point = round(random.uniform(0.2, 0.6), 2)
        end_point = round(random.uniform(0.7, 0.9), 2)
        duration = round(random.uniform(0.5, 0.8), 2)
        self.poco.swipe([start_point, end_point], [start_point, end_point - 0.6], duration=duration)

    def lottery(self):
        # self.poco(name="com.songheng.eastnews:id/jv").click()
        # self.poco(name="com.songheng.eastnews:id/mv", text="幸运转盘").wait(10).click()

        i = 0
        while i < 20:
            self.poco(name="J_gift").wait(5).click()

            try:
                click_gain = self.poco(name="gainBtn", desc="立即领取").wait(10)
                if click_gain.exists():
                    click_gain.click()
                else:
                    self.poco(name="gainBtn", text="立即翻倍").wait(5).click()

                print("开始转动..")
            except Exception as e:
                print(str(e))
                try:
                    self.poco(name="com.songheng.eastnews:id/apj").wait(5).click()
                    print("关闭广告")
                except Exception as e:
                    print("看视频")
                    self.poco(name="gainBtn").click()
                    time.sleep(40)

                    # 关闭视频广告
                    adv_close = self.poco(name="com.songheng.eastnews:id/go").wait(5)
                    if adv_close.exists():
                        adv_close.click()
                    else:
                        self.poco(name="com.songheng.eastnews:id/tt_video_ad_close").wait(5).click()

                    self.poco(name="gainBtn").wait(5).click()

    def close_push_news(self):

        if self.poco("com.songheng.eastnews:id/x8").exists():
            print("遇到推送新闻，退出")
            self.poco("com.songheng.eastnews:id/wz").click()


if __name__ == '__main__':
    eastNews = EastNews()
    # eastNews.run()
    # eastNews.get_top_title_coin()
    # eastNews.lottery()
    eastNews.watch_video()
    # eastNews.watch_news()
