# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_saveUserPhoneBookList.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/2/19 
"""
import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
import json
import time
from common.FrogHeader import FrogHeader
from testcases import FrogLogin
from utils.Logger import Logger
from utils.AESCipher import AESCipher
from utils.Loggers import Loggers
from testcases.FrogLogin import login_fb
from config.FrogConf import UserName
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()

yml = ymlUtil().get["frog"]['api']['metab']['saveUserPhoneBook']

class TestSavePhoneBook:
    @staticmethod

    def bookList_CN(maxNum, telHead, tName):

        # tel = r"""{"friendOLKList": "[{\"eName\":\"%s\",\"telPhone\":\"0086%s\"}]"}"""% (eName, telPhone)
        phoneBookList = []
        num = 0
        for i in range(0, maxNum):
        # {eName:\\" fan\\",telPhone:\\"15032515105\\"}

            telNum = "{}{:05d}".format(telHead, num)
            telName = "{}{:03d}".format(tName, num)
            telDic = {}
            telDic["eName"] = telName
            telDic["telPhone"] = telNum
            num += 1
            # telP = str(telDic).replace('\'', '\"')
            phoneBookList.append(telDic)#telP

        phoneBook = """{"friendOLKList":\"%s\"}""" % phoneBookList

        tel = phoneBook.replace("\'", "\\\"")

        return tel
    def test_saveUserPhoneBookList(self, login_fb):
        tel = TestSavePhoneBook.bookList_CN(maxNum=10, telHead=158001, tName="B-")
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['saveUserPhoneBookListApi']
        data = tel
        logger.info("上传通讯录接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("saveUserPhoneBookList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0