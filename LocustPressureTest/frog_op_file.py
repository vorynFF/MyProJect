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
import random

from FrogHeader import FrogHeader
from FrogRequest import frog_req

tel_to_userid = []
host = "https://test.frogcool.com"


class LoginTaskSet(TaskSet):
    """登陆调试"""

    # wait_time = between(1, 3)

    def __init__(self, parent):
        super().__init__(parent)
        self.sId = ''
        self.id = ''
        self.token = ''

    def on_start(self):
        print("Executing on_start ...")
        """ 用户登录 """
        self.username = None
        self.areacode = None
        try:
            logininfo = self.user.queue_data.get()
            items = logininfo.split("|")
            self.username = items[1]
            self.areacode = items[0]
            # print(f"username: {username}")
            # self.user.queue_data.put_nowait(username)
        except Exception as e:
            print(e)
            print("Queue is empty.")
        if not self.username:
            exit(1)
        # 发送短信验证码
        msg_path = "/growAlong/v1/api/common/sendSmsV3"
        header = FrogHeader.get_header()
        data = {
            "areaCode": self.areacode,  # 区号
            "code": "login",
            "type": "mobile",
            "userName": self.username  # 登陆手机号
        }
        # self.client.headers.update(header)
        # response = self.client.post(msg_path, json=data)
        response = frog_req.post(host + msg_path, headers=header, json=data)
        print("send_msg:{}".format(response))
        # print(response.status_code)
        # 验证短信登陆
        login_path = "/growAlong/v1/api/common/validSmsCode"
        header = FrogHeader.get_header()
        login_data = {
            "areaCode": self.areacode,  # 区号
            "code": "login",
            "smsCode": "1111",  # 验证码
            "type": "mobile",
            "userName": self.username  # 登陆手机号
        }
        # self.client.headers.update(header)
        # res = self.client.post(login_path, json=login_data)
        res = frog_req.post(host + login_path, headers=header, json=login_data)
        try:
            print(res["body"])
            data_obj = res["body"]["data"]["dataObject"]
            self.sId = data_obj["sId"]
            self.id = res["body"]["userId"]
            self.token = data_obj["token"]
        except Exception as e:
            print("res:{}, {}".format(self.username, res))
            print(self.username + str(e))

    def on_stop(self):
        #"退出登录接口"
        print("Executing on_stop ...")

        # api = "/growAlong/v1/api/user/admin/logout"
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = self.sId
        # header["userId"] = "{}".format(self.id)
        # header["token"] = self.token
        # self.client.headers.update(header)
        # # data = """{"queryType": "v1_gift"}"""
        #
        # res = self.client.post(api)
        # # print("=============开始=================")
        # # print("friendList:{}".format(res.json()))
        # assert res.status_code == 200
        # body = res.json()
        # # print(body)
        # # print(self.username)
        # try:
        #     assert body["state"]["code"] == 0
        #     print(body["state"]["msg"])
        # except:
        #     print(self.username + api + res)
        #     print(body["state"]["code"])
        #     print(body["state"]["msg"])

    @task
    def getVideoUserInfo(self):
        if self.token == '':
            return
        index = random.randint(0, len(tel_to_userid) - 1)
        api = "/growAlong/v2/api/user/getVideoUserInfo?videoUserId=" + tel_to_userid[index]  # 77945126
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        # res = self.client.post(api)
        # assert res.status_code == 200
        # body = res.json()
        # # print(body)
        # assert body["state"]["code"] == 0
        with self.client.post(api, catch_response=True) as response:
            if response.status_code == 200:
                body = response.json()
                if body["state"]["code"] == 0:
                    response.success()
                else:
                    response.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                response.failure('Failured:{}'.format(response.status_code))


class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
    # host = "http://192.168.2.129"
    # 初始化参数化队列
    queue_data = queue.Queue()
    file = open("user_info.sql", "r")
    content = file.readlines()
    for line in content:
        print(line)
        items = line.split("|")
        print(len(items))
        if len(items) == 4:
            key = items[2].strip()
            value = items[0].strip()
            area = items[1].strip()
            tel_to_userid.append(value)
            # tel_to_userid[key] = value
            userinfo = area + "|" + key
            queue_data.put_nowait(userinfo)
    print(len(tel_to_userid))
    print(queue_data)
    # queue_data.put_nowait("15800000054")
    # queue_data.put_nowait("15800000055")
    # queue_data.put_nowait("13900030000")
    # queue_data.put_nowait("13900040000")
    # queue_data.put_nowait("13900050000")
    # queue_data.put_nowait("13900060000")
    # queue_data.put_nowait("13900070000")
    # queue_data.put_nowait("13900080000")
    # queue_data.put_nowait("13900090000")
    # queue_data.put_nowait("13900100000")


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f frog_op_file.py --web-host="127.0.0.1" --host=https://test.frogcool.com')
