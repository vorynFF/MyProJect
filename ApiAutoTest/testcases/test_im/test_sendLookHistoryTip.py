# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_sendLookHistoryTip.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/8 
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
from testcases.FrogLogin import login_fb
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['im']['sendLookHistoryTip']


class TestSendLookHistoryTip:
    def test_sendLookHistoryTip(self, login_fb):
        # 云信消息已读提示接口，点击消息记录时调用
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        #
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        data = {"friendUserId":33769113}
        print("header:{}".format(header))
        url = frog["host"] + yml['sendLookHistoryTipApi']
        logger.info("云信消息已读提示接口")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("LookHistoryTip:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
