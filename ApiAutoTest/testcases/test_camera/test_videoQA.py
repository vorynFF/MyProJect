# -*- coding: UTF-8 -*-
"""
@Project ：FrogApiAutoTest
@File    ：test_whatsUp.py
@IDE     ：PyCharm
@Author  ：yuhang
@Date    ：2021/12/9 下午5:11
"""
import random
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
from testcases.FrogLogin import login_yh, login_smy
from testcases.FrogLogin import login_yh_2
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['camera']['videoQA']


class TestVideoQA:

    def test_saveVideoQA(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        id_data = "{\"videoId\":15646742, \"questionUserId\":82632214, \"questionContent\":\"yu144144\", " \
                  "\"replyUserId\": 94561788} "
        url = frog["host"] + yml['saveVideoQaApi']
        logger.info("保存提问或者回答问题接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res["body"]["state"]["msg"] == "Operation succeeded;Operation succeeded"

    def test_getVideoQAList(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        #
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token

        header = login_yh
        print("header:{}".format(header))
        url = frog["host"] + yml['getVideoQAListApi']
        logger.info("获取匿名提问记录列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        findRespVoList = res["body"]["data"]["findRespVoList"]
        questionContents = []
        for question in findRespVoList:
            questionContents.append(question["questionContent"])
        assert 'yu144144' in questionContents

    def test_weather(self, login_smy):
        header = login_smy
        print("header:{}".format(header))
        # Longitude： 经度坐标
        # latitude： 纬度坐标
        Longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        url = frog["host"] + yml['weatherApi'] + "/{}/{}".format(round(latitude, 2), round(Longitude, 2))
        logger.info("保存提问或者回答问题接口")
        res = frog_req.post(url, headers=header)
        logger.info("res:{}".format(res))
        print(res)
        assert res['code'] == 200
        assert res['body']['data']['conditionCode'] != []


if __name__ == '__main__':
    x = round(random.uniform(-180, 180), 2)
    y = round(random.uniform(-90, 90), 2)
    print(x, y)
