# -*- coding: UTF-8 -*-
'''
@Project ：FrogAndroidMonkeyTest 
@File    ：FrogWdaTestStart.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/8/27 7:39 下午 
'''
import subprocess
import threading

class FrogWdaTestStart(threading.Thread):
    def __init__(self, web_driver_agent):
        threading.Thread.__init__(self)

        self.inner_start = False

    def run(self):
        print("开始线程：" + self.name)
        test_out_str = subprocess.getoutput(self.test_cmd)
        print(test_out_str)
        if "iproxy" in test_out_str:
            self.inner_start = False
        else:
            print("inner start")
            # 内部启动的xcodebuild，在测试这边要有一个等待时间和一个kill操作
            self.inner_start = True
            subprocess.getoutput(self.iproxy)
        print("退出线程：" + self.name)