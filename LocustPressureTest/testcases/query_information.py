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
        self.friendUserid = MyTeskGroup.tel_to_frienduserid[a]
        if self.friendUserid == self.id:
            if a > 0:
                self.friendUserid = MyTeskGroup.tel_to_frienduserid[a][a - 1]
            else:
                self.friendUserid = MyTeskGroup.tel_to_frienduserid[a][a + 1]

    def on_stop(self):
        print("Executing on_stop ...")

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
    def getVideoPlayInfo(self):
        """旧视频播放"""
        api = "/growAlong/v1/api/video/getVideoPlayInfo?videoId=1555"
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
    def getSysMsgList(self):
        """系统消息列表"""
        api = "/growAlong/v1/api/index/getSysMsgList"
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
    def getFriendOLK(self):
        """通讯录列表"""
        api = "/growAlong/v1/api/friend/getFriendOLK"
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
    def getFriendMsgUserList(self):
        """已关注的好友用户列表"""
        api = "/growAlong/v1/api/user/getFriendMsgUserList"
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
    def getFriendMsgUserListV2(self):
        """已关注的好友用户列表 包含最近联系人"""
        api = "/growAlong/v1/api/user/getFriendMsgUserListV2"
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
    def getIndexFriendNewMsgList(self):
        """最新在线用户动态，万马奔腾"""
        api = "/growAlong/v1/api/index/getIndexFriendNewMsgList"
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
    def getTagTypeSelectList(self):
        """标签类型选择列表"""
        api = "/growAlong/v1/api/videoTag/getTagTypeSelectList"
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
    def getUserENameList(self):
        """搜索用户"""
        api = "/growAlong/v1/api/search/getUserENameList?selectValue=zhang1"
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
    def getFriendList(self):
        """好友列表"""
        api = "/growAlong/v1/api/user/getFriendList"
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
    def getMutualFriendList(self):
        """可能认识页面MutualFriendS列表"""
        api = "/growAlong/v2/api/user/getMutualFriendList?videoUserId=77945126"
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
    def getToolkitTxt(self):
        """Toolkit页面展示"""
        api = "/growAlong/v1/api/user/getToolkitTxt"
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
    def getBestFriendOfList(self):
        """可能认识页面best列表"""
        api = "/growAlong/v2/api/user/getBestFriendOfList?videoUserId=77945126"
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
    def getUserAddFriendLeaderboardList(self):
        """用户关注好友分数排行榜"""
        api = "/growAlong/v2/api/leaderboard/getUserAddFriendLeaderboardList"
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
    def getUserVlogVideoListV2(self):
        """旧单用户主页日常视频列表"""
        api = "/growAlong/v1/api/video/getUserVlogVideoListV2"
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
    def getVideoQAList(self):
        """视频匿名问题列表"""
        api = "/growAlong/v1/api/videoQA/getVideoQAList"
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
    def getUserAuthCardsList(self):
        """获取卡片认证信息"""
        api = "/growAlong/v1/api/userCards/getUserAuthCardsList"
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
    os.system('locust -f query_information.py --web-host="127.0.0.1" --host=https://test.frogcool.com')