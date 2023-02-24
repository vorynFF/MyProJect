# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：TestDemo.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/14 11:49 下午 
'''

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
from testcases.FrogLogin import login_fb, login_sls

import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['pond']['pondList']


class TestPond:
    def test_mock_client(self, login_fb):
        url = yml['indexMsgUnreadNumberApi']
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
        host = "https://test.frogcool.com"
        # frog_req = FrogRequest()
        res = frog_req.post(host + url, headers=header)
        print(res)
        assert res['code'] == 200

    allure.story("获取谁把userid加为best friend")
    def test_getFriendsList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        api = "/growAlong/v1/api/friend/getFriendsList"
        header = FrogHeader.get_header()
        # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + api
        logger.info("获取共同好友接口请求")
        res = frog_req.post(url, headers=header)
        logger.info("FriendList:{}".format(res))
        assert res['code'] == 200
        friendLists = res['body']['data']
        assert len(friendLists) > 0
        target_friend = None
        for friend in friendLists:
            if friend['eName'] == "macklutest":
                target_friend = friend
                break
        assert target_friend is not None
        key = "rC5bF3tR7mP1rX1k"
        aes_cipher = AESCipher(key)
        friend_user_id = aes_cipher.decrypt(target_friend["friendUserId"])
        assert friend_user_id == '77945126'

    def test_getPondVideoList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # yunXinIM_accid = dataObj["yunXinIM_accid"]
        # yunXinIM_token = dataObj["yunXinIM_token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        # data = {
        #     "userId": id
        # }
        url = frog["host"] + yml['getPondVideoListApi']
        # frog_req = FrogRequest()
        # 统计30次请求，总共有多少人重复Aaa
        allUserDict = dict()
        for i in range(50):
            tmpUserDict = dict()  # 单次请求里面，有多少个重复的froggers
            res = frog_req.post(url, headers=header)
            print("pond:{}".format(res))
            pondDataEn = res["body"]["data"]
            # 解码
            key = "rC5bF3tR7mP1rX1k"
            aes_cipher = AESCipher(key)
            pondData = aes_cipher.decrypt(pondDataEn)
            pondDataDict = json.loads(pondData)
            print(pondData)
            if pondDataDict["ext1"] == '16':
                findRespVoList = pondDataDict["findRespVoList"]
                for respVo in findRespVoList:
                    videoUserId0 = respVo["videoUserId"]
                    videoUserName = respVo["videoUserEName"]
                    videoUserId = videoUserName + ":" + videoUserId0
                    # 单次请求的重复情况
                    if videoUserId in tmpUserDict.keys():
                        tmpUserDict[videoUserId] = tmpUserDict[videoUserId] + 1
                    else:
                        tmpUserDict[videoUserId] = 1
                    # 总的
                    if videoUserId in allUserDict.keys():
                        allUserDict[videoUserId] = allUserDict[videoUserId] + 1
                    else:
                        allUserDict[videoUserId] = 1
            for key, value in tmpUserDict.items():
                if value > 1:
                    logger.info("第{}次获取，有重复froggers:{},重复: {} 次".format(i, key, value))
            # print(pondDataDict)
            time.sleep(0.05)
        for key, value in allUserDict.items():
            if value > 1:
                logger.info("有重复froggers:{},重复: {} 次".format(key, value))
        print(len(allUserDict))
        print(allUserDict)

    def test_getVideoRepeated(self, login_sls):
        header = login_sls
        url = frog["host"] + yml['getVideoRepeatedListApi'] + "?page=3&pageSize=10&hasMore=true"
        print(url)
        data = {'videoId': '89905269'}
        res = frog_req.post(url, headers=header, data=data)
        print(res)
        C1 = res['body']['data']
        key = "rC5bF3tR7mP1rX1k"
        d = AESCipher(key).decrypt(C1)

