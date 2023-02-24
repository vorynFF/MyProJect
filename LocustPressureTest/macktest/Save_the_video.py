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
        #print(videourl)
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
        #print("=============开始=================")
        #print("friendList:{}".format(res.json()))
        assert res.status_code == 200
        body = res.json()
        #print(body)
        #print(self.username)
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
    os.system('locust -f Save_the_video.py --web-host="127.0.0.1" --host=https://test.frogcool.com')