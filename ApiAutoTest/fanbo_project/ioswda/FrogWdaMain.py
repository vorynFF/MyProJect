# -*- coding: UTF-8 -*-
'''
@Project ：FrogAndroidMonkeyTest 
@File    ：FrogWdaMain.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/8/27 9:55 下午 
'''
import time
import numpy as np
import pysnooper
import wda
from FrogMonkeyEvent import FrogMonkeyEvent
from FrogWdaCallFront import FrogWdaCallFront
from ThreadOp import stop_thread

from FrogWdaIproxyStart import FrogWdaTestStart

@pysnooper.snoop(output='./log/debug.log')


def getRandomPoint(window_size):
    randxy = np.random.rand(2)
    x = int(window_size.width * randxy[0])
    y = int(window_size.height * randxy[1])
    print(x, ",", y)
    return x, y


if __name__ == '__main__':
    d = wda.USBClient(udid="00008020-000211000C02003A", port=8100, wda_bundle_id="com.fanbo.WebDriverAgentRunner.xctrunner")  # 1.2.0 引入 wda_bundle_id 参数

    bundle_id = 'com.frog.lotus.en'
    s = d.session(bundle_id)

    # 启动一个线程，如果应用在后台，切换到前台
    frogFront = FrogWdaCallFront(s, bundle_id)
    frogFront.start()
    # s.xpath('//*[@label="Tab Bar"]/Button[2]').click()
    # 设定monkey测试参数
    # monkey产生事件数
    event_count = 50
    # tap事件占比
    tap_count = 70
    # 滑动事件占比
    swipe_count = 25
    # 长按事件占比
    hold_count = 5
    # 事件之间的delay事件，单位秒
    delay_time = 0.2
    frogEvent = FrogMonkeyEvent(d, event_count, tap_count, swipe_count, hold_count, delay_time)
    frogEvent.monkey_run()

    # 停止后台调用前台进程
    stop_thread(frogFront)
    # for i in range(0, 100):
    #     # x, y = getRandomPoint(d.window_size())
    #     # d.tap(x, y)
    #     frogEvent.swipe()
    #     time.sleep(0.1)
    #     # state = s.app_state(bundle_id)
    #     # if state.value == 3:
    #     #     s.app_activate(bundle_id)
