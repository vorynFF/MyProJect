# -*- coding: UTF-8 -*-
'''
@Project ：FrogAndroidMonkeyTest 
@File    ：FrogMonkeyEvent.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/8/28 11:09 下午 
'''
import logging
import time

import numpy as np
from utils.Logger import Logger

logger = Logger().getlog()


class FrogMonkeyEvent(object):
    def __init__(self, wda, test_count, tap_rate, swipe_rate, hold_rate, delay_time=0.1):
        self.wda = wda
        self.window_size = wda.window_size()
        #
        self.delimeter = 10
        self.delay = delay_time
        self.totalRate = tap_rate + swipe_rate + hold_rate
        # 测试总次数
        self.test_count = test_count
        # 点击数百分比，比如55就表示55%
        self.tap_count = test_count * (tap_rate / self.totalRate)
        # 滑动数占比，比如30表示30%
        self.swipe_count = test_count * (swipe_rate / self.totalRate)
        # 长按占比
        self.hold_count = test_count * (hold_rate / self.totalRate)
        self.tap_index = tap_rate
        self.swipe_index = tap_rate + swipe_rate

    # 在屏幕范围内随机产生2个坐标点
    def __getRandomPoint(self):
        randxy = np.random.rand(2)
        x = int(self.window_size.width * randxy[0])
        y = int(self.window_size.height * randxy[1])
        return x, y

    # 点击
    def __tap(self):
        x, y = self.__getRandomPoint()
        logging.info("tap:({},{})".format(x, y))
        self.wda.tap(x, y)

    # 滑动
    def __swipe(self):
        x1, y1 = self.__getRandomPoint()
        x2, y2 = self.__getRandomPoint()
        # 尽量把x1,x2坐标不要靠近顶部，底部，避免切换应用
        if y1 < self.delimeter:
            y1 = y1 + self.delimeter
        if y2 < self.delimeter:
            y2 = y2 + self.delimeter
        if y1 + self.delimeter > self.window_size.height:
            y1 = y1 - self.delimeter
        if y2 + self.delimeter > self.window_size.height:
            y2 = y2 - self.delimeter
        logger.info("swipe:({},{})|({},{})".format(x1, y1, x2, y2))
        self.wda.swipe(x1, y1, x2, y2, 0.5)

    # 长按
    def __long_press(self):
        x, y = self.__getRandomPoint()
        logging.info("tap_hold:({},{})".format(x, y))
        self.wda.tap_hold(x, y)

    # monkey测试入口
    def monkey_run(self):

        for i in range(0, self.test_count):
            # 随机生成0-100之间的随机数
            random_count = 100 * np.random.rand(1)[0]
            # print("random:", random_count)
            if random_count <= self.tap_index:
                if self.tap_count > 0:
                    self.__tap()
                    self.tap_count = self.test_count - 1
                else:
                    if self.swipe_count > 0:
                        self.__swipe()
                        self.swipe_count = self.swipe_count - 1
                    elif self.hold_count > 0:
                        self.__long_press()
                        self.hold_count = self.hold_count - 1
            elif self.tap_index < random_count <= self.swipe_index:
                if self.swipe_count > 0:
                    self.__swipe()
                    self.swipe_count = self.swipe_count - 1
                else:
                    if self.tap_count > 0:
                        self.__tap()
                        self.tap_count = self.test_count - 1
                    elif self.hold_count > 0:
                        self.__long_press()
                        self.hold_count = self.hold_count - 1
            elif self.swipe_index < random_count:
                if self.hold_count > 0:
                    self.__long_press()
                    self.hold_count = self.hold_count - 1
                else:
                    if self.tap_count > 0:
                        self.__tap()
                        self.tap_count = self.test_count - 1
                    elif self.swipe_count > 0:
                        self.__swipe()
                        self.swipe_count = self.swipe_count - 1
            time.sleep(self.delay)
