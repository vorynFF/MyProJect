from locust import TaskSet, task, HttpUser, between, events
import queue
import time
import gevent
import os
import random
from FrogHeader import FrogHeader

class Theaddressbook(TaskSet):

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
        self.client.headers.update(header)
        response = self.client.post(msg_path, json=data)
        print("send_msg:{}".format(response))
        print(response.status_code)

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
        self.client.headers.update(header)
        res = self.client.post(login_path, json=login_data)
        print("登陆返回:{}, {}".format(self.username, res.json()))
        body = res.json()
        dataObj = body["data"]["dataObject"]
        self.sId = dataObj["sId"]
        self.id = body["userId"]
        self.token = dataObj["token"]

        """准备friendUserId"""
        a = random.randint(0, 1784)

        self.friendUserid = self.user.tel_to_frienduserid[a]
        if self.friendUserid == self.id:
            if a > 0:
                self.friendUserid = self.user.tel_to_frienduserid[a - 1]
            else:
                self.friendUserid = self.user.tel_to_frienduserid[a + 1]

    def on_stop(self):
        print("Executing on_stop ...")

    @task
    def saveFriendOLK(self):
        """保存通讯录"""
        api = "/growAlong/v1/api/friend/saveFriendOLK"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendOLKList": '[{"eName":"zhang 118","telPhone":"18232120001"},{"eName":"zhang119","telPhone":"18232120002"},{"eName":"zhang120","telPhone":"18232120003"},]',
            "eName": "z",
            "telPhone": "18232126335"
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def saveFriendOLK(self):
        """保存通讯录"""
        api = "/growAlong/v1/api/friend/saveFriendOLK"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendOLKList": '[{"eName":"zhang 118","telPhone":"18232120001"},{"eName":"zhang119","telPhone":"18232120002"},{"eName":"zhang120","telPhone":"18232120003"},]',
            "eName": "",
            "telPhone": ""
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def saveUserPhoneBookList(self):
        """导入通讯录接口"""
        api = "/growAlong/v1/api/friend/saveUserPhoneBookList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendOLKList": '[{"eName":"zhang 118","telPhone":"18232120001"},{"eName":"zhang119","telPhone":"18232120002"},{"eName":"zhang120","telPhone":"18232120003"},]'
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])
    @task
    def getFriendOLK(self):
        """通讯录列表"""
        api = "/growAlong/v1/api/friend/getFriendOLK"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])



    @task
    def getFriendsList(self):
        """Friends列表"""
        api = "/growAlong/v1/api/friend/getFriendsList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getFriendsList(self):
        """Friends列表"""
        api = "/growAlong/v1/api/friend/getFriendsList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getVideoUserInfo(self):
        """视频播放页面获取用户信息"""
        api = "/growAlong/v2/api/user/getVideoUserInfo?videoUserId=77945126"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getMutualFriendList(self):
        """可能认识页面MutualFriendS列表"""
        api = "/growAlong/v2/api/user/getMutualFriendList?videoUserId=77945126"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])


class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [Theaddressbook]
    """准备测试数据"""
    queue_data = queue.Queue()
    tel_to_frienduserid = []
    file = open(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + os.sep + "user_info.sql", "r")
    content = file.readlines()
    for line in content:
        items = line.split("|")
        if len(items) == 4:
            key = items[2].strip()
            value = items[0].strip()
            tel_to_frienduserid.append(value)
            area = items[1].strip()
            userinfo = area + "|" + key
            queue_data.put_nowait(userinfo)


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f the_address_book.py --web-host="127.0.0.1" --host=https://test.frogcool.com')