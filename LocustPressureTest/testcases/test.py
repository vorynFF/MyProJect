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



    def on_stop(self):
        print("Executing on_stop ...")


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
            "friendUserId": "33769113"
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



class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]
    """准备测试数据"""
    queue_data = queue.Queue()
    path = "./userid.sql"
    with open(path, "r") as file:

        content = file.readlines()
        for line in content:
            # print(line)
            items = line.split("|")
            if len(items) == 4:
                key = items[2].strip()
                value = items[0].strip()
                area = items[1].strip()
                userinfo = area + "|" + key
                queue_data.put_nowait(userinfo)


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f test.py --web-host="127.0.0.1" --host=https://test.frogcool.com')