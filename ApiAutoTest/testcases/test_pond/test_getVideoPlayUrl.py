# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_getVideoPlayUrl.py
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
import common.FrogSSHRedis as frogRedis
from db.FrogSSHMysqlHandle import MysqlHandle
import random

from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['pond']['videoPlayUrl']

class TestGetVideoPlayUrl:
    def test_getVideoPlayUrl(self, login_fb):      # 获取pond nominated列表接口
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        data = """{"videoId":21195650}"""
        url = frog["host"] + yml['getVideoPlayUrl']
        logger.info("视频播放前获取视频地址接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("VideoPlayUrl:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        assert res['body']['data']['videoUrl'] == 'https://dx265v3f1t09x.cloudfront.net/public/frog/android/video/TXVideo_1637150826560635b37323dbe409ba2e672a07ef42b1b1637150164979.mp4'

    def test_getPurchasedGiftsListV2(self, login_fb):
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        # data = """{"videoId":21195650}"""
        url = frog["host"] + yml['getPurchasedGiftsListV2Api']
        logger.info("购买礼物列表v2")
        res = frog_req.post(url, headers=header)
        logger.info("getPurchasedGiftsListV2:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        giftGetList = res['body']['data']['giftGetList']
        gift_id_list = []
        gift_name_list = []
        for i in giftGetList:
            gift_id_list.append(i['giftId'])
            gift_name_list.append(i['giftEName'])
        sql = "select gift_e_name from gift_info where id = {}".format(random.choice(gift_id_list))
        data = con.select(sql, one=True)
        assert len(data) > 0
        assert data[0] in gift_name_list