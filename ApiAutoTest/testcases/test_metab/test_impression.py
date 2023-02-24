# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_impression.py
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
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.Logger import Logger
from utils.AESCipher import AESCipher
from utils.Loggers import Loggers
from testcases.FrogLogin import login_fb
from testcases.FrogLogin import login

import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['metab']['impression']


class TestH5:
    def test_h5ImpressionSave(self):

        h5_data = """{
                "frogKey": "bMBFfi",
                "answerTxt": "h5test",
                "DID": "021efc3db0c43e7f60110ecee9fcd7ee"
                }"""
        h5_header = FrogHeader.get_ht_header()
        # 添加header数据

        print("h5_header:{}".format(h5_header))
        url = frog["host"] + yml['impressionSaveApi']
        logger.info("H5匿名印象提交接口")
        h5_res = frog_req.post(url, headers=h5_header, data=h5_data)
        logger.info("h5ImpressionSave:{}".format(h5_res))
        assert h5_res['code'] == 200
        h5DataList = h5_res['body']['data']
        assert h5DataList['eName'] == "15800000054"

    def test_saveImpressionMsg(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['saveImpressionMsgApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        data = """{"friendUserId": 58804776, "answerTxt": "pythontest"}"""
        url = frog["host"] + yml['saveImpressionMsgApi']
        logger.info("保存匿名印象")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("saveImpressionMsg:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['msg'] == "Operation succeeded;Operation succeeded"

    def test_getImpressionMsgList(self, login):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getImpressionMsgListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login
        print("header:{}".format(header))
        url = frog["host"] + yml['getImpressionMsgListApi']
        logger.info("获取匿名提问列表")
        res = frog_req.post(url, headers=header)
        logger.info("getImpressionMsgList:{}".format(res))
        assert res['code'] == 200
        impressionMsgList = res['body']['data']['findRespVoList']
        sql = "select " \
              "     id,answer_txt,  creat_time,msg_read_status,answer_user_id " \
              "from " \
              "     user_answer_rec " \
              "where user_id={} and del_flag='0' " \
              "order by creat_time desc".format(res['body']['userId'])
        data = con.select(sql, one=True)
        if data is None:
            assert res['body']['data']['findRespVoList'] == []
        else:
            assert data[1] == res['body']['data']['findRespVoList'][0]['answerTxt']

        # assert impressionMsgList[0]['answerTxt'] == "pythontest"
        # assert impressionMsgList[1]['answerTxt'] == "h5test"
        # assert impressionMsgList[1]['msgReadStatus'] == "0"   #校验未读状态，需要运行前两个接口
        # assert impressionMsgList[0]['msgReadStatus'] == "0"   #校验未读状态，需要运行前两个接口

    def test_delImpressionMsg(self, login_fb):
        header = login_fb
        url1 = frog["host"] + yml['getImpressionMsgListApi']
        logger.info("获取匿名提问列表")
        getImpressionMsg_res = frog_req.post(url1, headers=header)
        logger.info("getImpressionMsgList:{}".format(getImpressionMsg_res))
        assert getImpressionMsg_res['code'] == 200
        impressionMsgList = getImpressionMsg_res['body']['data']['findRespVoList']
        sql = "select " \
              "     id,answer_txt,  creat_time,msg_read_status,answer_user_id " \
              "from " \
              "     user_answer_rec " \
              "where user_id={} and del_flag='0' " \
              "order by creat_time desc".format(getImpressionMsg_res['body']['userId'])
        data = con.select(sql, one=True)
        if data is None:
            assert getImpressionMsg_res['body']['data']['findRespVoList'] == []
        else:
            assert data[1] == impressionMsgList[0]['answerTxt']
        url2 = frog["host"] + yml['delImpressionMsgApi']
        data = {
            "id": getImpressionMsg_res['body']['data']['findRespVoList'][0]['id']
        }
        delImpressionMsg_res = frog_req.post(url2, headers=header, json=data)
        assert delImpressionMsg_res['body']['state']['msg'] == "Operation succeeded;Operation succeeded"

    def test_h5QASave(self):
        h5_api = yml['QASaveApi']
        h5_data = """{
                "frogKey": "bMBFfi",
                "answerTxt": "pytest QA",
                "DID": "021efc3db0c43e7f60110ecee9fcd7ee"
                }"""
        h5_header = FrogHeader.get_ht_header()
        # 添加header数据

        print("h5_header:{}".format(h5_header))
        url = frog["host"] + h5_api
        logger.info("H5QA保存接口")
        h5_res = frog_req.post(url, headers=h5_header, data=h5_data)
        logger.info("QASave:{}".format(h5_res))
        assert h5_res['code'] == 200
