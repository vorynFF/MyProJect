# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_saveVideoBirthday.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/4 
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
from testcases.redistest import RedisTest
from db.FrogSSHMysqlHandle import MysqlHandle
import common.FrogSSHRedis as frogRedis
from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['pond']['videoBirthday']

class TestSaveVideoBirthday:
    # def redis(self, login_fb):
    #     dataObj = login_fb["body"]["data"]["dataObject"]
    #     sId = dataObj["sId"]
    #     id = login_fb["body"]["userId"]
    #     token = dataObj["token"]
    #     api = "/growAlong/v2/api/user/getRedisValue"
    #     header = FrogHeader.get_header()
    #     # 添加header数据
    #     header["sid"] = sId
    #     header["userId"] = "{}".format(id)
    #     header["token"] = token
    #     print("header:{}".format(header))
    #     data = """{"redisKey":"user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:%d", "type":"del"}"""% id
    #     url = frog["host"] + api
    #     logger.info("test")
    #     res = frog_req.post(url, headers=header, data=data)
    #     logger.info("test:{}".format(res))
    #     assert res['code'] == 200
    def saveVideoBirthday(self, login_fb):
        header = login_fb
        print("header:{}".format(header))
        data = """{"birthday": "1227332801000"}"""
        url = frog["host"] + yml['saveVideoBirthdayApi']
        logger.info("保存池塘年龄")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("saveVideoBirthday:{}".format(res))
        return res

    def test_saveVideoBirthday(self, login_fb):
        res = TestSaveVideoBirthday.saveVideoBirthday(self, login_fb)
        if res['body']['state']['msg'] == 'Please try again later ;Please try again later':
            # re_type = "del"
            # re_redisKey = "user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:"
            # RedisTest.redistest(self, login_fb, type=re_type, redisKey=re_redisKey)
            # RedisTest.redisDelBirth(self, login_fb)
            print(frogRedis.str_delete("user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:58804776"))
            res_r = TestSaveVideoBirthday.saveVideoBirthday(self, login_fb)
            assert res_r['code'] == 200
            assert res_r['body']['userId'] == 58804776
            assert res_r['body']['state']['msg'] == "Operation succeeded;Operation succeeded"
            assert res_r['body']['data'] == "13"
        else:
            assert res['code'] == 200
            assert res['body']['userId'] == 58804776
            assert res['body']['state']['msg'] == "Operation succeeded;Operation succeeded"
            assert res['body']['data'] == "14"