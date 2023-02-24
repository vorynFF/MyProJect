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

    def on_stop(self):
        print("Executing on_stop ...")


    @task
    def refresh(self):
        """更新用户及视频"""
        api = "/v1/user/29468478/refresh"
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}'.format(body))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def refresh(self):
        """获取推荐用户列表"""
        api = "/v1/recommend/29468478"
        with self.client.get(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}'.format(body))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def refresh(self):
        """获取推荐用户列表"""
        api = "/v1/recommend/mark/29468478"
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}'.format(body))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def refresh(self):
        """获取推荐用户列表"""
        api = "/v1/user/29468478//medias"
        with self.client.post(api, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["state"]["code"] == 0:
                    res.success()
                else:
                    res.failure('state code:{}'.format(body))
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
    os.system('locust -f algorithm.py --web-host="127.0.0.1" --host=http://52.15.118.149:8088')