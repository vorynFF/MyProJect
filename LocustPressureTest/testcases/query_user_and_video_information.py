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
        self.friendUserid = MyTeskGroup.tel_to_frienduserid[a]
        if self.friendUserid == self.id:
            if a > 0:
                self.friendUserid = MyTeskGroup.tel_to_frienduserid[a][a - 1]
            else:
                self.friendUserid = MyTeskGroup.tel_to_frienduserid[a][a + 1]

    def on_stop(self):
        print("Executing on_stop ...")


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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, json=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def getFriendUser(self):
        """好友信息"""
        api1 = "/growAlong/v1/api/friend/getFriendStatusInfo"
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
        with self.client.post(api, json=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200 or res.status_code == 30001:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, json=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))


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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, json=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, json=data, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def getPurchasedGiftsList(self):
        """已经购买了的礼物列表"""
        api1 = "/growAlong/v1/api/gift/getPurchasedGiftsList?giftType=v1_gift"
        api2 = "/growAlong/v1/api/gift/getPurchasedGiftsList?giftTypecommon_gift"
        a = random.randint(0,1)
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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))

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
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}, sid:{},uid:{}'.format(body, self.sId, self.id))
            else:
                res.failure('Failured:{}'.format(res.status_code))



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
    os.system('locust -f query_user_and_video_information.py --web-host="127.0.0.1" --host=https://test.frogcool.com')