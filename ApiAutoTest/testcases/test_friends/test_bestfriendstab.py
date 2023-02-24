# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_bestfriendstab.py
@IDE     ：PyCharm
@Author  ：fanbo
@Date    ：2021/12/1
"""

import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
import json
import time
from common.FrogHeader import FrogHeader
from utils.Logger import Logger
from utils.AESCipher import AESCipher
from utils.Loggers import Loggers
from testcases.FrogLogin import login_fb, login_whb
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['friends']['bestfriendstab']


class TestBestFriendsTab:
    def test_getIndexFriendListInfo(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getIndexFriendListInfoApi']
        logger.info("获取首页亲密好友信息接口")
        res = frog_req.post(url, headers=header)
        logger.info("IndexFriendListInfo:{}".format(res))
        assert res['code'] == 200

        bestFriendUserInfoList = res['body']['data']['bestFriendUserInfoList']
        assert len(bestFriendUserInfoList) > 0

        best_friend_list = None
        for bestFriend in bestFriendUserInfoList:
            if bestFriend['eName'] == "Kkkm":
                best_friend_list = bestFriend
                break

        assert best_friend_list is not None

        friend_user_id = best_friend_list['friendUserId']
        assert friend_user_id == 33769113
        return res

    def test_getAddBestFriendList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getAddBestFriendListApi']
        logger.info("获取被添加亲密好友列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getAddBestFriendList:{}".format(res))
        assert res['code'] == 200
        # assert id == res['body']['userId']
        addBestFriendList = res['body']['data']['findRespVoList']

        assert len(addBestFriendList) > 0
        add_best_friend = None
        for bestFriend in addBestFriendList:
            if bestFriend['eName'] == "85858585":
                add_best_friend = bestFriend
                break

        assert add_best_friend is not None

        friend_user_id = add_best_friend['friendUserId']

        assert friend_user_id == 85484422

    def test_addBestFriend(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['addBestFriendApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['addBestFriendApi']
        data = """{"friendUserId":"46555087"}"""
        logger.info("添加best friend接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("addBestFriend:{}".format(res))
        assert res['code'] == 200

        if res['body']['state']['code'] == 0:
            assert res['body']['data']['friendUserId'] == 46555087
            bestFriendId = res['body']['data']['id']
            get_res = TestBestFriendsTab.test_getIndexFriendListInfo(self, login_fb)
            bestFriendUserInfoList = get_res['body']['data']['bestFriendUserInfoList']
            best_friend_list = []
            for bestFriend in bestFriendUserInfoList:
                best_friend_list.append(bestFriend['friendUserId'])

            assert 46555087 in best_friend_list

        else:
            get_res = TestBestFriendsTab.test_getIndexFriendListInfo(self, login_fb)
            bestFriendUserInfoList = get_res['body']['data']['bestFriendUserInfoList']
            best_friend_list = None
            for bestFriend in bestFriendUserInfoList:
                if bestFriend['friendUserId'] == 46555087:
                    best_friend_list = bestFriend
                    break
            assert best_friend_list is not None
            bestFriendId = best_friend_list['id']
        return bestFriendId

    def test_delBestFriend(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['delBestFriendApi']
        bestFriendId = TestBestFriendsTab.test_addBestFriend(self, login_fb)
        data = """{"id":"%d"}""" % bestFriendId
        logger.info("删除best friend接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("delBestFriend:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        t = 0.1
        time.sleep(t)
        get_res = TestBestFriendsTab.test_getIndexFriendListInfo(self, login_fb)
        bestFriendUserInfoList = get_res['body']['data']['bestFriendUserInfoList']
        best_friend_list = []
        for bestFriend in bestFriendUserInfoList:
            best_friend_list.append(bestFriend['friendUserId'])

        assert 46555087 not in best_friend_list

    def test_updateBestFriend(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['updateBestFriendApi']
        del_data = {'type': 'del', 'friendUserId': '86724026'}
        logger.info("删除或者添加亲密好友合并接口")
        del_res = frog_req.post(url, headers=header, json=del_data)
        logger.info("updateBestFriend: {}".format(del_res))
        if del_res['body']['state']['msg'] != "Operation succeeded;Operation succeeded":
            add_data = {'type': 'add', 'friendUserId': '86724026'}
            add_res = frog_req.post(url, headers=header, json=add_data)
            logger.info("updateBestFriend: {}".format(add_res))
            assert add_res['body']['state']['msg'] == "Operation succeeded;Operation succeeded"
            aes_friendUserAccId = AESCipher("rC5bF3tR7mP1rX1k").decrypt(add_res['body']['data']['friendUserAccId'])
            assert aes_friendUserAccId == "frog_dev_86724026"


if __name__ == '__main__':
    pytest.main('-q test_bestfriendstab.py')
