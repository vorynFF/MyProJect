# -*- coding: UTF-8 -*-
'''
@Project ：Locust 
@File    ：login.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2022/2/17 8:34 下午 
'''
from locust import TaskSet, task, HttpUser, between, events
import queue
import time
import gevent
import os

from FrogHeader import FrogHeader


class LoginTaskSet(TaskSet):
    """登陆调试"""

    wait_time = between(0.1, 1)

    def on_start(self):
        print("Executing on_start ...")

    def on_stop(self):
        print("Executing on_stop ...")

    @task
    def login(self):
        """ 用户登录 压力测试 """
        self.areacode = 86
        self.username = None
        try:
            logininfo = self.user.queue_data.get()
            self.username = logininfo
        except Exception as e:
            print(e)
            print("Queue is empty.")
        if not self.username:
            print("Test is over.")
            exit(0)
        # 发送短信验证码
        msg_path = "/growAlong/v1/api/common/sendSmsV3"
        header = FrogHeader.get_header()
        data = {
            "areaCode": self.areacode,  # 区号
            "code": "register",
            "type": "mobile",
            "userName": self.username  # 登陆手机号
        }
        self.client.headers.update(header)
        with self.client.post(msg_path, json=data, catch_response=True) as response:
            # print("send_msg:{}".format(response))
            if response.status_code == 200:
                # 验证短信登陆
                login_path = "/growAlong/v1/api/common/validSmsCode"
                header = FrogHeader.get_header()
                login_data = {
                    "eName": self.username,
                    "areaCode": self.areacode,  # 区号
                    "code": "register",
                    "smsCode": "1111",  # 验证码
                    "type": "mobile",
                    "userName": self.username  # 登陆手机号
                }
                self.client.headers.update(header)
                with self.client.post(login_path, json=login_data, catch_response=True) as res:
                    print(res.content)
                    if res.status_code == 200:
                        body = res.json()
                        # print(body)
                        if body["state"]["code"] == 0 or body["state"]["code"] == 20005:
                            res.success()
                        else:
                            print(res.content)
                            res.failure('{},login code error:{},{}'.format(self.username, body["state"]["msg"],
                                                                           body["state"]["code"]))
                    else:
                        res.failure('login http_status_code error:{}'.format(res.status_code))

            else:
                response.failure("msg send failure")


class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
    # host = "http://192.168.2.129"
    # 初始化参数化队列
    prefix = "18620"
    queue_data = queue.Queue()
    for index in range(0, 200000):
        tmpstr = "{}".format(index)
        length = len(tmpstr)
        if length == 1:
            subfix = "00000" + tmpstr
        elif length == 2:
            subfix = "0000" + tmpstr
        elif length == 3:
            subfix = "000" + tmpstr
        elif length == 4:
            subfix = "00" + tmpstr
        elif length == 5:
            subfix = "0" + tmpstr
        else:
            subfix = tmpstr
        phone = prefix + subfix
        # print(phone)
        queue_data.put_nowait(phone)
    # queue_data.put_nowait("15800000054")


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f register.py --web-host="127.0.0.1" --host=https://test.frogcool.com')
    #delete from user_info where telphone like '18820%';
