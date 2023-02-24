# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：test_friends.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/20 7:41 下午 
'''
import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
from testcases.FrogLogin import login, login_whb, login_response, login_z

import json
from common.FrogHeader import FrogHeader
from utils.Loggers import Loggers
import allure
from utils.YmlUtil import ymlUtil

logger = Loggers()
# frog_req = FrogRequest()
allure.feature("测试好友相关接口")
yml = ymlUtil().get["frog"]['api']['friends']['friend']


class TestFriends:
    allure.story("获取谁把userid加为best friend")

    def test_getBestFriendOfList(self, login):
        # dataObj = login["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login
        print("header:{}".format(header))
        url = frog["host"] + yml['getBestFriendOfListApi'] + "?videoUserId=77945126"
        logger.info("获取共同好友接口请求")
        res = frog_req.post(url, headers=header)
        logger.info("bestFriendOfList:{}".format(res))
        assert res['code'] == 200

    allure.story("获取共同好友接口测试")

    def test_getMutualFriendList(self, login):
        allure.step("登陆，获取用户token，id等信息")
        # dataObj = login["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login["body"]["userId"]
        # token = dataObj["token"]
        # yunXinIM_accid = dataObj["yunXinIM_accid"]
        # yunXinIM_token = dataObj["yunXinIM_token"]

        # 77945126 是378020331@qq.com的userid，对应手机号：13721089003，通过登陆接口获取到
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login
        print("header:{}".format(header))
        url = frog["host"] + yml['getMutualFriendListApi'] + "?videoUserId=77945126"
        print(url)
        logger.info("获取共同好友接口请求")
        res = frog_req.post(url, headers=header)
        logger.info("friendList:{}".format(res))
        assert res["code"] == 200
        assert res["body"]["state"]["code"] == 0
        mutual_friend_list = res["body"]["data"]["findRespVoList"]
        assert len(mutual_friend_list) > 0
        logger.info("获取共同好友数据成功")
        print(json.dumps(res["body"]["data"], ensure_ascii=False, indent=1))

    allure.story("获取用户信息测试")

    def test_getVideoUserInfo(self, login):
        allure.step("登陆，获取用户token，id等信息")
        # dataObj = login["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login["body"]["userId"]
        # token = dataObj["token"]

        # 77945126 是378020331@qq.com的userid，对应手机号：13721089003，通过登陆接口获取到

        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login
        print("header:{}".format(header))
        url = frog["host"] + yml['getVideoUserInfoApi'] + "?videoUserId=77945126"
        logger.info("获取共同好友接口请求")
        res = frog_req.post(url, headers=header)
        logger.info("friendList:{}".format(res))
        assert res["code"] == 200
        assert res["body"]["state"]["code"] == 0
        # mutual_friend_list = res["body"]["data"]["findRespVoList"]
        # assert len(mutual_friend_list) > 0
        logger.info("获取共同好友数据成功")

    # def test_getFriendOLK(self, login_z):
    #     header = login_z
    #     print("header:{}".format(header))
    #     url = frog["host"] + yml['getFriendOLKApi']
    #     logger.info("获取通讯录接口请求")
    #     res = frog_req.post(url, headers=header)
    #     logger.info("getFriendOLK:{}".format(res))
    #     assert res["body"]["data"] != []
    #     assert res["body"]['state']['msg'] == "Operation succeeded;Operation succeeded"
    #     mutual_friend_list = res["body"]["data"]["findRespVoList"]
    #     print(type(mutual_friend_list))
    #     assert len(mutual_friend_list) > 0
    #     logger.info("获取通讯录好友数据成功")

    def test_attentionV2(self, login_whb):
        header = login_whb
        print("header:{}".format(header))
        url = frog["host"] + yml['attentionV2Api']
        data = {"userId": int(header['userId']), "friendUserId": 49753521}
        logger.info("attentionV2Api params: {}".format(data))
        res = frog_req.post(url, headers=header, json=data)
        logger.info("attentionV2Api response: {}".format(res))
        assert res["body"]['state']['msg'] == "Operation succeeded;Operation succeeded"
        assert res["body"]['data'] != ""

    def test_saveFriendOLK(self, login_response):
        dataObj = login_response["body"]["data"]["dataObject"]
        sId = dataObj["sId"]
        id = login_response["body"]["userId"]
        token = dataObj["token"]
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = sId
        header["userId"] = "{}".format(id)
        header["token"] = token
        print("header:{}".format(header))
        url = frog["host"] + yml['saveFriendOLKApi']
        friendList = [{"MALOyU": "18822113062", "爽爽": "15210371290"}]
        data = {"eName": dataObj['eName'], "telPhone": dataObj['telphone'], "friendOLKList": friendList}
        logger.info("saveFriendOLKApi params: {}".format(data))
        res = frog_req.post(url, headers=header, json=data)
        logger.info("saveFriendOLKApi response: {}".format(res))
        assert res["body"]['state']['msg'] == "Operation succeeded;Operation succeeded"
        assert res["body"]['data'] is not None

    # 新版关注确认接口
    def test_attentionConfirm(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['attentionConfirmApi']
        data = {'friendUserId': 86724026}
        res = frog_req.post(url, headers=header, json=data)
        logger.info("attentionConfirmApi params: {}".format(data))
        logger.info("attentionConfirmApi response: {}".format(res))
        assert res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert res['body']['data']['followStatus'] == '2'

    # request消息删除接口
    def test_delRequestMsg(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['delRequestMsgApi']
        data = {'friendUserId': 86724026}
        res = frog_req.post(url, headers=header, json=data)
        logger.info("attentionConfirmApi params: {}".format(data))
        logger.info("attentionConfirmApi response: {}".format(res))
        assert res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'




