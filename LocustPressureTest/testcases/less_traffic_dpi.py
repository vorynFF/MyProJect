# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：less_traffic_dpi.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/2/21 
"""
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
            data_obj = res["body"]["data"]["dataObject"]
            self.sId = data_obj["sId"]
            self.id = res["body"]["userId"]
            self.token = data_obj["token"]
        except Exception as e:
            print("res:{}, {}".format(self.username, res))
            print(self.username + str(e))

    def on_stop(self):
        "退出登录接口"
        print("Executing on_stop ...")

        api = "/growAlong/v1/api/user/admin/logout"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        # data = """{"queryType": "v1_gift"}"""

        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
            print(body["state"]["msg"])
        except:
            print(self.username + api + res)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getGiftInfoList(self):
        """获取可以兑换的礼物列表接口"""
        api = "/growAlong/v1/api/gift/getGiftInfoList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = """{"queryType": "v1_gift"}"""

        with self.client.post(api, data=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                print(body)
                if body["state"]["code"] == 0 or body["state"]["code"] == 20005:
                    res.success()
                else:
                    print(body)
                    res.failure('{},login code error:{},{}'.format(self.username, body["state"]["msg"],
                                                                   body["state"]["code"]))
            else:
                res.failure('login http_status_code error:{}'.format(res.status_code))
    @task
    def getTagTypeList(self):
        """获取主题大分类列表接口"""
        api = "/growAlong/v1/api/videoTag/getTagTypeList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)

        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                print(body)
                if body["state"]["code"] == 0 or body["state"]["code"] == 20005:
                    res.success()
                else:
                    print(body)
                    res.failure('{},login code error:{},{}'.format(self.username, body["state"]["msg"],
                                                                   body["state"]["code"]))
            else:
                res.failure('login http_status_code error:{}'.format(res.status_code))

    @task
    def getVideoPlayUrl(self):
        """视频播放前获取视频地址接口"""
        api = "/growAlong/v1/api/video/getVideoPlayUrl"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = """{"videoId": "32568484"}"""

        with self.client.post(api, data=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                print(body)
                if body["state"]["code"] == 0 or body["state"]["code"] == 20005:
                    res.success()
                else:
                    print(body)
                    res.failure('{},login code error:{},{}'.format(self.username, body["state"]["msg"],
                                                                   body["state"]["code"]))
            else:
                res.failure('login http_status_code error:{}'.format(res.status_code))

    @task
    def getVideoPlayUrl(self):
        """好友日常用户信息列表接口"""
        api = "/growAlong/v1/api/video/getVlogUserRecList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        # data = """{"videoId": "32568484"}"""

        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                print(body)
                if body["state"]["code"] == 0 or body["state"]["code"] == 20005:
                    res.success()
                else:
                    print(body)
                    res.failure('{},login code error:{},{}'.format(self.username, body["state"]["msg"],
                                                                   body["state"]["code"]))
            else:
                res.failure('login http_status_code error:{}'.format(res.status_code))
class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
    # host = "http://192.168.2.129"
    # 初始化参数化队列
    queue_data = queue.Queue()
    file = open(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + os.sep + "user_info.sql", "r")
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
if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f less_traffic_dpi.py --web-host="127.0.0.1" --host=https://test.frogcool.com')