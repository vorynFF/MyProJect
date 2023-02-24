# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_gettag.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/3 
"""

import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
import json
import time
import random
from common.FrogHeader import FrogHeader
from testcases import FrogLogin
from utils.Logger import Logger
from utils.AESCipher import AESCipher
from utils.Loggers import Loggers
from testcases.FrogLogin import login_fb
import allure
import common.FrogSSHRedis as frogRedis
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['friends']['gettag']


class TestGetTag:
    def test_getTagTypeSelectList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token

        header = login_fb
        id = int(header['userId'])
        tagTypeId = random.randint(1, 3)
        data = {"tagTypeId": "{}".format(tagTypeId)}
        print("header:{}".format(header))
        url = frog["host"] + yml['getTagTypeSelectListApi']
        logger.info("获取视频拍摄标签选择列表接口（带分页）")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("TagTypeList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id

        redis_name = "user:videoTag:{}:getTagSubListRanking".format(tagTypeId)
        redis_count = frogRedis.zset_getcount(redis_name)  # 获取redis中总数
        assert redis_count == res['body']['data']['tagSubListMap']['toTalSize']
        redis_max = frogRedis.zset_getmax(redis_name)  # 获取redis中分数最高的数据信息
        redis_max_info = eval(redis_max[0][0])
        videoTagList = res['body']['data']['tagSubListMap']['findVideoTagList']
        assert redis_max_info['tagId'] == videoTagList[0]['tagId']
        # tag_list = None
        #
        # for videoTag in videoTagList:
        #     if videoTag['tagValue'] == '2021':
        #         tag_list = videoTag
        #         break
        # tagList = tag_list['tagId']
        # assert tagList == 477

    def test_getTagTypeList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['getTagTypeListApi']
        logger.info("获取tag类型接口")
        res = frog_req.post(url, headers=header)
        logger.info("getTagTypeList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        dataList = res['body']['data']
        assert len(dataList) > 0
        sql = "select id,tag_type_c_name,tag_type_e_name,fire_size from tag_type_info where tag_type_del='0' and id = {} order by tag_type_sort;".format(dataList[0]['id'])
        data = con.select(sql, one=True)
        assert dataList[0]['tagTypeCName'] == data[1]

