from locust import TaskSet, task, HttpUser, between, events
import queue
import time
import gevent
import os
import random
from FrogHeader import FrogHeader

class LoginTaskSet(TaskSet):


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
        a = random.randint(0,1784)

        self.friendUserid = self.user.tel_to_frienduserid[a]
        if self.friendUserid == self.id:
            if a > 0:
                self.friendUserid = self.user.tel_to_frienduserid[a - 1]
            else:
                self.friendUserid = self.user.tel_to_frienduserid[a + 1]


    def on_stop(self):
        print("Executing on_stop ...")

    @task
    def sendRequestMsg(self):
        """Request消息发送"""
        api = "/growAlong/v1/api/friend/sendRequestMsg"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid,
            "msgTxt": "123"
        }
        res = self.client.post(api, json=data)
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
    def saveUserInfo(self):
        """修改用户信息"""
        api = "/growAlong/v1/api/user/saveUserInfo"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        a = random.randint(0,1)
        b1 = "test"
        b2 = time.time()
        b = b1+str(b2)
        data = {
            "id": self.id,
            "telphone": self.username,
            "gender": a,
            "eName": b,
            "birthday": ""
                            }
        res = self.client.post(api, json=data)
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
    def savePushReg(self):
        """保存推送token"""
        api = "/growAlong/v1/api/user/savePushReg"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "pushTokens": ""
        }
        res = self.client.post(api, json=data)
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
    def readIndexMsg(self):
        """消息已读"""
        api = "/growAlong/v1/api/index/readIndexMsg"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        """
        msgId  单个消息id，单个消息已读时传
        readType	读取消息类型，single：单个消息已读，msgId为必传；all，全部消息已读
        msgType     消息类型，friend：好友消息，sysMsg：系统消息 ，self_vlog：好友日常消息（传friendUserId为当前用户id）
        friendUserId    好友用户id，好友消息时必传
        """
        data = {
            "readType": "all",
            "msgType": "",
            "friendUserId": ""
                            }
        res = self.client.post(api, json=data)
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
    def addVideoLike(self):
        """视频点赞"""
        api = "/growAlong/v1/api/video/addVideoLike?videoId=63130171"
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
"""
    @task
    def saveVideoBirthday(self):
        保存年龄
        api = "/growAlong/v1/api/videoPond/saveVideoBirthday?birthday="
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
"""

class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
    """准备测试数据"""
    tel_to_frienduserid = []
    queue_data = queue.Queue()
    file = open(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + os.sep + "user_info.sql", "r")
    content = file.readlines()
    for line in content:
        #print(line)
        items = line.split("|")
        if len(items) == 4:
            key = items[2].strip()
            value = items[0].strip()
            area = items[1].strip()
            tel_to_frienduserid.append(value)
            userinfo = area + "|" + key
            queue_data.put_nowait(userinfo)



if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f save_user_information.py --web-host="127.0.0.1" --host=https://test.frogcool.com')