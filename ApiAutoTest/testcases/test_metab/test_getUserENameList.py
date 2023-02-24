# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_getUserENameList.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/14 
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
import common.FrogSSHRedis as frogRedis
from db.FrogSSHMysqlHandle import MysqlHandle
import random

from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['metab']['userEnameList']


class TestGetUserENameList:
    def test_getUserEnameList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['userEnameListApi']
        rom = random.randint(5000, 30000)
        selectValue_sql = "select id, frog_id, e_name from user_info where frog_id is not null and e_name != '' limit {}, 1".format(
            rom)
        data = con.select(selectValue_sql, one=True)
        selectValue = data[random.randint(1, 2)]
        req_json = {"selectValue": selectValue}
        logger.info("搜索好友列表")
        res = frog_req.post(url, headers=header, json=req_json)
        logger.info("getUserENameList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        userSearchList = res['body']['data']['userSearchList']
        userIdList = []
        assert len(userSearchList) > 0
        for i in userSearchList:
            userIdList.append(i['userId'])
        assert data[0] in userIdList
