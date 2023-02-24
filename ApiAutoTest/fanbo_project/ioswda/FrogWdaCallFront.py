# -*- coding: UTF-8 -*-
'''
@Project ：FrogAndroidMonkeyTest 
@File    ：FrogAppCallFront.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/7/29 5:35 下午 
'''
import os
import threading
import time


class FrogWdaCallFront(threading.Thread):
    def __init__(self, s, bundle_id):
        threading.Thread.__init__(self)
        self.s = s
        self.bundle_id = bundle_id

    def run(self):
        print("定时将app前置的线程：" + self.name)
        while True:
            state = self.s.app_state(self.bundle_id)
            if state.value == 3:
                self.s.app_activate(self.bundle_id)
                time.sleep(30)
        print("定时将app前置线程结束：" + self.name)
