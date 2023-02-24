# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：FrogRequest.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/14 9:53 上午 
'''
import requests
from utils.Logger import Logger
from requests_pkcs12 import Pkcs12Adapter
from config.FrogConf import p12


class FrogRequest:
    def __init__(self):
        self.log = Logger().getlog()
        self.session = requests.session()

    def requests_api(self, url, params=None, data=None, json=None, method="get", **kwargs):
        r = ""
        if "aws" in str(url):
            self.session.mount(url, Pkcs12Adapter(pkcs12_filename=p12["p12_cert"], pkcs12_password=p12["p12_pw"]))
            if method == "get":
                # get请求
                self.log.debug("发送get请求")
                r = self.session.get(url, params=params, **kwargs)
            elif method == "post":
                # post请求
                self.log.debug("发送post请求")
                r = self.session.post(url, data=data, json=json, **kwargs)
        else:
            if method == "get":
                # get请求
                self.log.debug("发送get请求")
                r = requests.get(url, params=params, **kwargs)
            elif method == "post":
                # post请求
                self.log.debug("发送post请求")
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
