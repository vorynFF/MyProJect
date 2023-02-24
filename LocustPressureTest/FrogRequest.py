# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：FrogRequest.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/14 9:53 上午 
'''
import requests


class FrogRequest:
    def __init__(self):
        self.tag = "locust"

    def requests_api(self, url, params=None, data=None, json=None, method="get", **kwargs):

        if method == "get":
            # get请求
            r = requests.get(url, params=params, **kwargs)
        elif method == "post":
            # post请求
            r = requests.post(url, data=data, json=json, **kwargs)

        # 获取结果内容
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 字典返回
        return res

    def get(self, url, params=None, **kwargs):
        return self.requests_api(url, params=params, method="get", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.requests_api(url, data=data, json=json, method="post", **kwargs)


frog_req = FrogRequest()
