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
    def attentionV2(self):
        """添加好友"""
        api = "/growAlong/v1/api/friend/attentionV2"
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

        """确认添加好友"""
        api = "/growAlong/v1/api/friend/attentionConfirm"
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
    def getGiftInfoList(self):
        if self.token == '':
            return
        """获取可以兑换的礼物列表接口"""
        api = "/growAlong/v1/api/gift/getGiftInfoList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = """{"queryType": "v1_gift"}"""

        with self.client.post(api, data=data, catch_response=True) as response:
            if response.status_code == 200:
                body = response.json()
                if body["state"]["code"] == 0:
                    response.success()
                else:
                    response.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                response.failure('Failured:{}'.format(response.status_code))

    @task
    def getTagTypeList(self):
        if self.token == '':
            return
        """获取主题大分类列表接口"""
        api = "/growAlong/v1/api/videoTag/getTagTypeList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)

        with self.client.post(api, catch_response=True) as response:
            if response.status_code == 200:
                body = response.json()
                if body["state"]["code"] == 0:
                    response.success()
                else:
                    response.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                response.failure('Failured:{}'.format(response.status_code))

    @task
    def getVideoPlayUrl(self):
        if self.token == '':
            return
        """视频播放前获取视频地址接口"""
        api = "/growAlong/v1/api/video/getVideoPlayUrl"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = """{"videoId": "32568484"}"""

        with self.client.post(api, data=data, catch_response=True) as response:
            if response.status_code == 200:
                body = response.json()
                if body["state"]["code"] == 0:
                    response.success()
                else:
                    response.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                response.failure('Failured:{}'.format(response.status_code))

    @task
    def getVideoPlayUrl(self):
        """好友日常用户信息列表接口"""
        if self.token == '':
            return
        api = "/growAlong/v1/api/video/getVlogUserRecList"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        # data = """{"videoId": "32568484"}"""

        with self.client.post(api, catch_response=True) as response:
            if response.status_code == 200:
                body = response.json()
                if body["state"]["code"] == 0:
                    response.success()
                else:
                    response.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                response.failure('Failured:{}'.format(response.status_code))

    @task
    def getRequestMsgList(self):
        """Request用户列表"""
        api = "/growAlong/v1/api/friend/getRequestMsgList"
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
    def getVideoPlayInfo(self):
        """旧视频播放"""
        api = "/growAlong/v1/api/video/getVideoPlayInfo?videoId=63130171"
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
    def getSysMsgList(self):
        """系统消息列表"""
        api = "/growAlong/v1/api/index/getSysMsgList"
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
    def getFriendMsgUserList(self):
        """已关注的好友用户列表"""
        api = "/growAlong/v1/api/user/getFriendMsgUserList"
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
    def getFriendMsgUserListV2(self):
        """已关注的好友用户列表 包含最近联系人"""
        api = "/growAlong/v1/api/user/getFriendMsgUserListV2"
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
    def getTagTypeSelectList(self):
        """标签类型选择列表"""
        api = "/growAlong/v1/api/videoTag/getTagTypeSelectList"
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
    def getUserENameList(self):
        """搜索用户"""
        api = "/growAlong/v1/api/search/getUserENameList?selectValue=zhang1"
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
    def getFriendList(self):
        """好友列表"""
        api = "/growAlong/v1/api/user/getFriendList"
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

    @task
    def getToolkitTxt(self):
        """Toolkit页面展示"""
        api = "/growAlong/v1/api/user/getToolkitTxt"
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
    def getBestFriendOfList(self):
        """可能认识页面best列表"""
        api = "/growAlong/v2/api/user/getBestFriendOfList?videoUserId=77945126"
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
    def getUserAddFriendLeaderboardList(self):
        """用户关注好友分数排行榜"""
        api = "/growAlong/v2/api/leaderboard/getUserAddFriendLeaderboardList"
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
    def getUserVlogVideoListV2(self):
        """旧单用户主页日常视频列表"""
        api = "/growAlong/v1/api/video/getUserVlogVideoListV2"
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
    def getVideoQAList(self):
        """视频匿名问题列表"""
        api = "/growAlong/v1/api/videoQA/getVideoQAList"
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
    def getUserAuthCardsList(self):
        """获取卡片认证信息"""
        api = "/growAlong/v1/api/userCards/getUserAuthCardsList"
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
    def indexMsgUnreadNumber(self):
        """未读消息数"""
        api = "/growAlong/v1/api/index/indexMsgUnreadNumber"
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
    def getFriendStatusInfo(self):
        """获取用户好友状态"""
        api = "/growAlong/v1/api/friend/getFriendStatusInfo"
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
    def getFriendUser(self):
        """好友信息"""
        api1 = "/growAlong/v1/api/friend/getFriendStatusInfo?friendUserId="
        api2 = self.id
        api = api1 + str(api2)
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
    def getUser(self):
        """当前登录用户信息"""
        api = "/growAlong/v1/api/user/getUser"
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
    def getVideoRecordInfo(self):
        """录制视频前信息展示"""
        api = "/growAlong/v1/api/video/getVideoRecordInfo"
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
    def getUserAccBalance(self):
        """用户余额"""
        api = "/growAlong/v1/api/user/getUserAccBalance"
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
    def getFriendVlogList(self):
        """IM用户日常视频播放列表"""
        api = "/growAlong/v1/api/vlog/getFriendVlogList"
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
        # print(body["state"]["code"])
        a = int(body["state"]["code"])
        # print(type(a))
        try:
            assert a in [0, 30001]
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getWhatsUpStatus(self):
        """whatsUpStatus状态"""
        api = "/growAlong/v1/api/friend/getWhatsUpStatus"
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
    def getUserShakeRecUserInfoList(self):
        """whatsUp记录"""
        api = "/growAlong/v1/api/shake/getUserShakeRecUserInfoList"
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
    def quickAddList(self):
        """推荐用户列表"""
        api = "/growAlong/v1/api/friend/quickAddList"
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
    def getRegAddFriendList(self):
        """注册后关联好友关系列表"""
        api = "/growAlong/v2/api/userRegFriend/getRegAddFriendList"
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
    def getUserNominatedList(self):
        """pond Nominated 列表接口"""
        api = "/growAlong/v1/api/multiple/getUserNominatedList"
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
    def getRequestFriendMsgList(self):
        """Request单好友聊天记录"""
        api = "/growAlong/v1/api/friend/getRequestFriendMsgList"
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
    def getPurchaseList(self):
        """ios充值商品列表"""
        api = "/growAlong/v1/api/coursePackage/getPurchaseList?queryType=cybermoney_en_iOS"
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
    def getPurchaseList(self):
        """Android充值商品列表"""
        api = "/growAlong/v1/api/coursePackage/getPurchaseList?queryType=cybermoney_en_Android"
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
    def getMsgChatStatus(self):
        """是否真聊天状态"""
        api = "/growAlong/v1/api/friend/getMsgChatStatus"
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
    def getPurchasedGiftsList(self):
        """已经购买了的礼物列表"""
        api1 = "/growAlong/v1/api/gift/getPurchasedGiftsList?giftType=v1_gift"
        api2 = "/growAlong/v1/api/gift/getPurchasedGiftsList?giftTypecommon_gift"
        a = random.randint(0, 1)
        if a == 0:
            api = api1
        elif a == 1:
            api = api2
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
    def getIndexFriendListInfo(self):
        """MutualFriend页面请求"""
        api = "/growAlong/v1/api/index/getIndexFriendListInfo"
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
    def getPurchasedGiftsListV2(self):
        """已经购买了的礼物V2"""
        api = "/growAlong/v1/api/gift/getPurchasedGiftsListV2"
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
    def getImpressionMsgList(self):
        """匿名印象列表"""
        api = "/growAlong/v1/api/impression/getImpressionMsgList"
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
    def getIndexMsgRecListV2(self):
        """点赞，送礼，好友请求列表"""
        api1 = "/growAlong/v1/api/index/getIndexMsgRecListV2?queryType=vote_video"
        api2 = "/growAlong/v1/api/index/getIndexMsgRecListV2?queryType=apply_add_friend"
        api3 = "/growAlong/v1/api/index/getIndexMsgRecListV2?queryType=gift"
        api4 = "/growAlong/v1/api/index/getIndexMsgRecListV2?queryType=video_cheer"
        a = random.randint(0, 3)
        if a == 0:
            api = api1
        elif a == 1:
            api = api2
        elif a == 2:
            api = api3
        else:
            api = api4
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
        assert res.status_code == 200
        body = res.json()
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
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "type": "user_thank",
            "friendUserId": 77945126
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
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
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "type": 77945126,
            "reportType": 18232126335
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
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
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
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
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        data = {
            "friendUserId": self.friendUserid
        }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
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
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def saveVideoV2(self):
        """保存视频"""
        api = "/growAlong/v1/api/video/saveVideoV2"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        videourl1 = "public/frog/ios/video/iOS_TXUGC_20220218_1645185373294_"
        t = time.time()
        videourl2 = round(t * 1000000)
        videourl3 = ".mp4"
        videourl = videourl1+str(videourl2)+videourl3
        data = {
                    "videoType": "mp4",
                    "stickersQAType": "anonymous1",
                    "coordinateUserMention": "[\\n\\n]",
                    "friendUserIds": "",
                    "videoImg": "",
                    "durating": "1",
                    "upVideoSite": "S3",
                    "clientUpTime": "2022-02-18 19:56:24",
                    "userId": self.id,
                    "coordinateTag": "{\\n\\n}",
                    "videoSize": "191991",
                    "QAFlag": "0",
                    "videoUrl": videourl,
                    "videoDes": "iOS upload successful",
                    "sendType": "self_vlog_pond",
                    "coordinateQA": "",
                    "fileId": "aliVideo"
                            }
        res = self.client.post(api, json=data)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

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

    @task
    def getPondVideoList(self):
        """池塘视频列表"""
        api = "/frogVideoPond/api/v1/video/Pond/getPondVideoList"
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
    def getUserUnreadVlogVideoList(self):
        """日常动态单用户未读视频播放列表"""
        api = "/frogVideoPond/api/v1/user/video/getUserUnreadVlogVideoList"
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
    def getUserVideoPlayInfo(self):
        """视频播放详情"""
        api = "/frogVideoPond/api/v1/user/video/getUserVideoPlayInfo?videoId=63130171"
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
    def getUserVlogVideoList(self):
        """个人主页视频播放列表"""
        api = "/frogVideoPond/api/v1/user/video/getUserVlogVideoList"
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
    def getUserPondVideoList(self):
        """单用户池塘视频播放列表"""
        api = "/frogVideoPond/api/v1/video/Pond/getUserPondVideoList"
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
    def getUserNewsVlogVideoList(self):
        """最新好友动态视频播放列表"""
        api = "/frogVideoPond/api/v1/user/video/getUserNewsVlogVideoList"
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
    def getPondVideoListOne(self):
        """池塘视频一次缓存列表"""
        api = "/frogVideoPond/api/v1/video/Pond/getPondVideoListOne"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getUserPondTagVideoList(self):
        """单用户标签视频列表"""
        api = "/frogVideoPond/api/v1/video/Pond/getUserPondTagVideoList?tagId=477"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getPondTagVideoList(self):
        """标签视频列表"""
        api = "/frogVideoPond/api/v1/video/Pond/getPondTagVideoList?tagId=477"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def saveAppOnlineTime(self):
        """保存最近在线时间"""
        api = "/growAlong/v2/api/user/saveAppOnlineTime"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getUserNewsVlogVideoUnreadList(self):
        """获取有未读视频用户播放列表接口"""
        api = "/frogVideoPond/api/v1/user/video/getUserNewsVlogVideoUnreadList"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getUserNewsVlogVideoReadList(self):
        """获取已读视频用户动态播放列表接口"""
        api = "/frogVideoPond/api/v1/user/video/getUserNewsVlogVideoReadList"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getUserVlogCreateVideoList(self):
        """合成视频列表接口"""
        api = "/frogVideoPond/api/v1/user/video/getUserVlogCreateVideoList"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        self.client.headers.update(header)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def updateBestFriendAdd(self):
        """添加亲密好友接口"""
        api = "/growAlong/v1/api/bestFriend/updateBestFriend"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        data = {
            "friendUserId": self.friendUserid,
            "type": "add"
        }
        self.client.headers.update(header, json=data)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def updateBestFriendDel(self):
        """添加亲密好友接口"""
        api = "/growAlong/v1/api/bestFriend/updateBestFriend"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        data = {
            "friendUserId": self.friendUserid,
            "type": "del"
        }
        self.client.headers.update(header, json=data)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])

    @task
    def getRegisterUserPhoneBook(self):
        """添加亲密好友接口"""
        api = "/growAlong/v1/api/friend/getRegisterUserPhoneBook"
        header = FrogHeader.get_header()
        header["sid"] = self.sId
        header["userId"] = "{}".format(self.id)
        header["token"] = self.token
        data = {
            "friendOLKList": '[{"eName":"zhang0002","telPhone":"18232120002"},{"eName":"zhang0003","telPhone":"18232120003"},{"eName":"zhang0004","telPhone":"18232120004"},]'
        }
        self.client.headers.update(header, json=data)
        res = self.client.post(api)
        assert res.status_code == 200
        body = res.json()
        try:
            assert body["state"]["code"] == 0
        except:
            print(api)
            print(body["state"]["code"])
            print(body["state"]["msg"])





class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
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
    os.system('locust -f all.py --web-host="127.0.0.1" --host=https://test.frogcool.com')