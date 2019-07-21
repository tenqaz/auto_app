# -*- coding: utf-8 -*-

__author__ = 'Jim'

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import random
import time

poco = AndroidUiautomationPoco()


def watch_video():
    poco("com.baidu.minivideo:id/index_feed_item_cover").click()
    time.sleep(10)

    swipe_num = 0

    while True:

        # 滑动
        print("下一个视频")
        x_pos = round(random.uniform(0.5, 0.9), 2)
        y_pos = round(random.uniform(0.85, 0.75), 2)
        duration = round(random.uniform(0.1, 0.2), 2)
        poco.swipe([x_pos, y_pos], [x_pos - 0.05, y_pos - 0.7], duration=duration)

        # 广告跳过
        if poco("com.baidu.minivideo:id/ad_flag_image").exists():
            print("广告跳过")
            continue

        # 看视频
        print("正在看视频..")
        watch_time = round(random.uniform(16, 20), 2)
        time.sleep(watch_time)
        print("看完该视频")

        if swipe_num > 30:
            break
        swipe_num += 1

    print("看完了30个视频，结束")


if __name__ == '__main__':
    watch_video()
