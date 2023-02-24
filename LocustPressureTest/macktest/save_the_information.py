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
    def sendLookHistoryTip(self):
        """IM查看历史"""
        api = "/growAlong/v1/api/friend/sendLookHistoryTip"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
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
    def saveUserShake(self):
        """whatsUp消息接口时发送的IM消息格式"""
        api = "/growAlong/v1/api/shake/saveUserShake"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
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
    def saveToolkitTxt(self):
        """保存视频人脸贴纸文字接口"""
        api = "/growAlong/v1/api/user/saveToolkitTxt"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "id": 0,
            "toolkitType": "faceTxt"
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
    def delQuickAdd(self):
        """删除推荐列表里用户"""
        api = "/growAlong/v1/api/friend/delQuickAdd"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
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
    def sendVideoStart(self):
        """IM视频发送开始"""
        api = "/growAlong/v1/api/video/sendVideoStart"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserIds": 77945126,
            "videoSrc": "test",
            "type": "start"
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
    def sendExpression(self):
        """感谢和表情接口"""
        api = "/growAlong/v1/api/gift/sendExpression"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "type": "user_thank",
            "friendUserId": 77945126
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
    def reportAndBlacklist(self):
        """拉黑举报好友"""
        api = "/growAlong/v1/api/user/reportAndBlacklist"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "type": 77945126,
            "reportType": 18232126335
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
    def addBestFriend(self):
        """新增亲密好友"""
        api = "/growAlong/v1/api/bestFriend/addBestFriend"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
        }
        res = self.client.post(api, json=data)
        # print("=============开始=================")
        # print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        # print(body)
        # print(self.username)
        try:
            assert body["state"]["code"] in [0, 30019]
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def unsubscribe(self):
        """取消关注用户"""
        api = "/growAlong/v1/api/friend/unsubscribe"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
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
    def smsInviteSave(self):
        """短信邀请"""
        api = "/growAlong/v2/api/userRegFriend/smsInviteSave?telPhone=18232126335"
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
    def saveFriendOLK(self):
        
        api = "/growAlong/v1/api/friend/saveFriendOLK"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendOLKList": "",
            "eName": 77945126,
            "telPhone": 18232126335
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
    def updateChatStatus(self):
        api = "/growAlong/v1/api/friend/updateChatStatus"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": 77945126,
            "chatStatus": 18232126335
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
"""

"""
    @task
    def saveUserPhoneBookList(self):
        api = "/growAlong/v1/api/friend/saveUserPhoneBookList?friendOLKList=zzz"
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



#   @task
#   def ignoreUserShake(self):
#      """忽略whatsUp"""
#     api = "/growAlong/v1/api/shake/ignoreUserShake"
#     header = FrogHeader.get_header()
#    # 添加header数据
#   header["sid"] = self.sId
#  header["userId"] = "{}".format(self.id)
#   header["token"] = self.token
#   self.client.headers.update(header)
#  data = {
#      "friendUserId": self.friendUserid
#  }
# res = self.client.post(api, json=data)
# print("=============开始=================")
# print("friendList:{}".format(res.json()))
#  assert res.status_code == 200
# body = res.json()
# print(body)
# print(self.username)
# try:
#       assert body["state"]["code"] == 0
#  except:
#     print(api)
#     print(body["state"]["code"])
#    print(body["state"]["msg"])

"""
    @task
    def saveImpressionMsg(self):
        api = "/growAlong/v1/api/impression/saveImpressionMsg"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
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
    os.system('locust -f save_the_information.py --web-host="127.0.0.1" --host=https://test.frogcool.com')