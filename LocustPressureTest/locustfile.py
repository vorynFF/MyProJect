# -*- coding: UTF-8 -*-
'''
@Project ：Locust 
@File    ：locustfile.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/9/25 5:27 下午 
'''
from locust import HttpUser, TaskSet, task
import os
import time
import hashlib
import json


class GetResume(HttpUser):
    min_wait = 100
    max_wait = 500

    def on_start(self):
        print("start working")

    # @task(1)  # 设置权重值，默认为1，值越大，优先执行
    def mock_client(self):
        # 如果后台需要的是json格式，需要加header，否则报415
        cur_time = str(int(round(time.time() * 1000)))
        print(cur_time)
        appSecret = "ff71f1d41ac7"
        json_param = {"attach": "thisisattach", "body": "hello", "convType": "PERSON", "eventType": "1",
                      "fromAccount": "111",
                      "fromClientType": "IOS", "fromDeviceId": "thisisfromdeviceid", "fromNick": "mike",
                      "msgTimestamp": cur_time, "msgType": "TEXT", "msgidClient": "1234567", "msgidServer": "3456789",
                      "resendFlag": "0", "to": "222"}

        # md5计算
        strbody = json.dumps(json_param)
        m = hashlib.md5()
        m.update(strbody.encode(encoding="utf-8"))
        str_md5 = m.hexdigest()
        # checksum计算
        sha_str = appSecret + str_md5 + cur_time
        sha = hashlib.sha1()
        sha.update(sha_str.encode(encoding="utf-8"))
        check_sum = sha.hexdigest()
        header = {"Content-Type": "application/json",
                  "CurTime": cur_time,
                  "MD5": str_md5,
                  "CheckSum": check_sum}
        self.client.headers.update(header)
        url1 = "/growAlong/v1/api/yunXinIM/mockClient"
        # 网上是直接把Json的格式填进去，但是在本项目中报400，无法识别数据格式，查看系统报错才明白需要转成json对象
        req = self.client.post(url1, json=json_param)
        print(req)
        if req.status_code == 200:
            print("success")
        else:
            print("fail")

    @task(1)
    def indexMsgUnreadNumber(self):
        url = "/growAlong/v1/api/index/indexMsgUnreadNumber"
        header = {
            "Connection": "keep-alive",
            "country": "2",
            "sign": "4c32daeea9c2207c39e70d575ed3ee38",
            "language": "en",
            "userid": "48002321",
            "platform": "android",
            "sid": "12536e217e0e452db28fa62054792a55",
            "encrypt": "md5",
            "connection": "close",
            "content-type": "application/x-www-form-urlencoded",
            "id": "1631611762867",
            "fpnv": "false",
            "ver": "244",
            "token": "E+mkL3PS+cijdXNZWTlzrQ==",
            "ex": "{\"sciso\": \"cn\", \"ctime\": \"2021-09-13 13:05:18\", \"locale\": \"CN\", \"nciso\": \"cn\", \"mac\": \"\",\"manufacturer\":\"Xiaomi\"}",
            "etag": "2f0ec04def7242358b3aebd23866bf951631096623587",
            "caller": "app",
            "timestamp": "1631611762867"
        }
        self.client.headers.update(header)
        req = self.client.post(url)
        print(req.text)
        if req.status_code == 200:
            print("success")
        else:
            print("fail")


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f locustfile.py --web-host="127.0.0.1" --host=https://test.frogcool.com')
    # 分布式执行
    # os.system('locust -f locustfile.py --web-host="127.0.0.1" -u 3000 -r 100 --host=http://18.166.156.104:8088'
    #           ' --master --master-bind-host 127.0.0.1 --master-bind-port 8090 ')
#
# #启动5个work试试
# for i in range(0,5):
#     os.system('locust -f locustfile.py --worker --master-host 127.0.0.1 --master-port 8090')
