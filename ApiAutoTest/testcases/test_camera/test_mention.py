# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_mention.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/2/16 
"""
from utils.YmlUtil import ymlUtil

"/v2/api/mention/getUserMentionMsgPageList"

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
import FrogSSHRedis
from db.FrogSSHMysqlHandle import MysqlHandle

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['camera']['mention']

class TestMention:
    def test_getUserMentionMsgPageList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # print("token:" + token)
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['getUserMentionMsgPageListApi']
        logger.info("用户VideoMention好友消息列表")
        res = frog_req.post(url, headers=header)
        logger.info("getUserMentionMsgPageList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        findRespVoList = res['body']['data']['findRespVoList']
        print("findRespVoList：" + str(findRespVoList))
        assert len(findRespVoList) > 0
        sql = "select video_id from  user_video_mention_rec where friend_user_id = {} and user_id = {} group by video_id".format(
            id, findRespVoList[0]['userId'])
        data = con.select(sql, one=True)
        assert data[0] == findRespVoList[0]['videoId']
