# -*- coding: UTF-8 -*-
"""
@Project ：FrogApiAutoTest
@File    ：test_whatsUp.py
@IDE     ：PyCharm
@Author  ：yuhang
@Date    ：2021/12/9 下午5:11
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
from testcases.FrogLogin import login_yh, login_whb
from testcases.FrogLogin import login_fb55
from testcases.FrogLogin import login_yh_2


import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()

isWhatsUpMag = "false"
yml = ymlUtil().get["frog"]['api']['im']['whatsUp']


class TestWhatsUp:
    def test_getUserShakeRecUserInfoList(self, login_fb55):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb55
        print("header:{}".format(header))
        url = frog["host"] + yml['getUserShakeRecUserInfoListApi']
        logger.info("获取可能认识页面MutualFriendS列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        ShakeList = res["body"]["data"]["findRespVoList"]
        print(ShakeList)
        skList = []
        for bf in ShakeList:
            skList.append(bf["userEName"])
        print(skList)
        assert 'Kkkm' in skList

    def test_getWhatsUpStatus(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getWhatsUpStatusApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        id_data = "{\"friendUserId\":\"82632214\"}"
        url = frog["host"] + yml['getWhatsUpStatusApi']
        logger.info("获取好友的whatsUpStatus状态接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res["body"]["state"]["msg"] == "Operation succeeded;Operation succeeded"
        global isWhatsUpMag
        isWhatsUpMag = res["body"]["data"]["isWhatsUpMag"]

    def test_saveUserShake(self, login_yh_2):
        # dataObj = login_yh_2["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh_2["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['saveUserShakeApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh_2
        print("header:{}".format(header))
        id_data = "{\"friendUserId\":\"94561788\"}"
        url = frog["host"] + yml['saveUserShakeApi']
        logger.info("whatsUp消息发送接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res["body"]["state"]["msg"] == "Operation succeeded;Operation succeeded"

    def test_ignoreUserShake(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['ignoreUserShakeApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        id_data = "{\"friendUserId\":\"82632214\"}"
        url = frog["host"] + yml['ignoreUserShakeApi']
        logger.info("whatsUp消息忽略接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res["body"]["state"]["msg"] == "Operation succeeded;Operation succeeded"

    def test_isWhatsUpMag(self, login_yh_2, login_yh):
        TestWhatsUp.test_getWhatsUpStatus(self, login_yh)
        if isWhatsUpMag == "false":  # 如果没有被摇手则发送摇手
            TestWhatsUp.test_saveUserShake(self, login_yh_2)
            TestWhatsUp.test_getWhatsUpStatus(self, login_yh)
            assert isWhatsUpMag == "true"
        elif isWhatsUpMag == "true":  # 如果被摇手则忽略摇手
            TestWhatsUp.test_ignoreUserShake(self, login_yh)
            TestWhatsUp.test_getWhatsUpStatus(self, login_yh)
            assert isWhatsUpMag == "false"

    # whatsUp 敲击接口
    def test_quitImShake(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['quitImShakeApi']
        data = {'friendUserId': 86724026}
        logger.info("attentionConfirmApi params: {}".format(data))
        res = frog_req.post(url, headers=header, json=data)
        logger.info("attentionConfirmApi response: {}".format(res))
        assert res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'



if __name__ == '__main__':
    pytest.main("q test_whatsUp.py")
