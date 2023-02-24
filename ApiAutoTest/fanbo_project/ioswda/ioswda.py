# -*- coding: UTF-8 -*-
'''
@Project ：FrogAndroidMonkeyTest 
@File    ：ioswda.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/8/22 8:44 上午 
'''
import time

import wda

from FrogWdaIproxyStart import FrogWdaTestStart

dumpxmlurl = 'http://localhost:8100/session/44DE6598-5137-4EF0-8E15-EA095E05DE86/source'

bundle_id = 'com.frog.lotus.en'
d = wda.Client('http://localhost:8100')
print(d.status())
s = d.session(bundle_id)
print(s.session_id)
time.sleep(3)
s.xpath('//*[@label="Tab Bar"]/Button[1]').click()
e = d.xpath('//XCUIElementTypeNavigationBar').get()
print(s.source())
# print(s.source(accessible=True))
print(e.info)
print(e.bounds)
g = s(name="FrogBestFriendListMainView").get()
print("g:", g.name)
print("g.rect", g.bounds)
f = s(className="XCUIElementTypeTabBar").get()
print("f:", f.info)
# print(e.frame)
time.sleep(3)
s.xpath('//*[@label="Tab Bar"]/Button[2]').wait(3).click()
print(s.xpath('//*[@label="Tab Bar"]/Button[2]'))
time.sleep(3)
d.screenshot('/Users/macklu/screen.png')

d.click(594, 2349)

# s.app_stop(bundle_id)
print(s.window_size())
d.click(340, 750)
time.sleep(1)
s(labelContains='edit').click()
time.sleep(3)
# 返回
e = s(labelContains="bottom back")
x = e.bounds.x + e.bounds.width / 2
y = e.bounds.y + e.bounds.height / 2
print(e.bounds.x)
print("x,y={},{}".format(x, y))
# d.tap(x, y)
d.click(int(x), int(y))
# d.click(0.501, 0.873)
time.sleep(2)
print("scale:",s.scale)
print(s.app_state(bundle_id))

d.home()
time.sleep(3)
print("home后的状态")
print(s.app_state(bundle_id))

s.app_terminate(bundle_id)
time.sleep(3)
print(s.app_state(bundle_id))
s.app_start(bundle_id)
print(s.app_state(bundle_id))
# wda先实现 monkey测试；1）测试运行自动启动：命令行启动；2）iproxy 8100 8100 线程启动；
# 启动frog，获取屏幕尺寸，获取主要几个bar的位置。 记住每个自页面的NavigationBar 导航栏的名字。
# 启动：xcodebuild -project /Users/macklu/Frog/wda/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=`idevice_id -l | head -n1`" test
# frog_start = FrogWdaTestStart("")