# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：redistest.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/10 
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
logger = Loggers()
video_group = {
    "lessTwelve": "lessTwelve", # <= 12
    "thirteenToSixteen": "thirteenToSixteen", # [13 - 16]
    "fourteenToEighteen": "fourteenToEighteen", # [14 - 18]
    "fifteenToTwentyOne": "fifteenToTwentyOne", # [15 - 21]
    "sixteenToTwentyOne": "sixteenToTwentyOne", # [16 - 21]
    "seventeenToTwentyOne": "seventeenToTwentyOne", # [17 - 21]
    "moreEighteen": "moreEighteen"# >= 18
}
class RedisTest:
    def redistest(self, login_fb, redisKey, type):
        dataObj = login_fb["body"]["data"]["dataObject"]
        sId = dataObj["sId"]
        id = login_fb["body"]["userId"]
        token = dataObj["token"]
        api = "/growAlong/v2/api/user/getRedisValue"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = sId
        header["userId"] = "{}".format(id)
        header["token"] = token
        print("header:{}".format(header))
        data = """{"redisKey":"%s%d", "type":"%s"}""" % (redisKey, id, type)
        url = frog["host"] + api
        logger.info("test")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("test:{}".format(res))
        assert res['code'] == 200

    def redisDelBirth(self, login_fb):
        dataObj = login_fb["body"]["data"]["dataObject"]
        sId = dataObj["sId"]
        id = login_fb["body"]["userId"]
        token = dataObj["token"]
        api = "/growAlong/v2/api/user/getRedisValue"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = sId
        header["userId"] = "{}".format(id)
        header["token"] = token
        print("header:{}".format(header))
        redisKey = "user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:"
        type = "del"
        data = """{"redisKey":"%s%d", "type":"%s"}""" % (redisKey, id, type)
        url = frog["host"] + api
        logger.info("test")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("test:{}".format(res))
        assert res['code'] == 200


    def testtests(self, login_fb):
        dataObj = login_fb["body"]["data"]["dataObject"]
        sId = dataObj["sId"]
        id = login_fb["body"]["userId"]
        token = dataObj["token"]
        api = "/growAlong/v2/api/user/getRedisValue"
        header = FrogHeader.get_header()
        # 添加header数据
        header["sid"] = sId
        header["userId"] = "{}".format(id)
        header["token"] = token
        print("header:{}".format(header))
        redisKey = "videoPond:data:pond:video:group:userListVideoScore:moreEighteen:"
        type = "zset"
        data = """{"redisKey":"%s%d", "type":"%s"}""" % (redisKey, id, type)
        url = frog["host"] + api
        logger.info("test")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("test:{}".format(res))
        assert res['code'] == 200


# 视频分组
# String
# lessTwelve = "lessTwelve"; // <= 12
# String
# thirteenToSixteen = "thirteenToSixteen"; // [13 - 16]
# String
# fourteenToEighteen = "fourteenToEighteen"; // [14 - 18]
# String
# fifteenToTwentyOne = "fifteenToTwentyOne"; // [15 - 21]
# String
# sixteenToTwentyOne = "sixteenToTwentyOne"; // [16 - 21]
# 默认
# String
# seventeenToTwentyOne = "seventeenToTwentyOne"; // [17 - 21]
# String
# moreEighteen = "moreEighteen"; // >= 18
#
#
# 年龄限制
# 查询类型：string
# 删除类型：del
# user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:[userId]
#
# 当前用户获取的列表对应用户id，类型：zset
# videoPond:data:pond:video:group:userGetUserList:33767067
# 当前用户获取的用户对应视频id
# 类型：hash
# videoPond:data:pond:video:group:userGetVideoList:33767067
# 单用户视频列表
# 类型：zset
# videoPond:data:pond:video:group:userListVideoScore:fourteenToEighteen:33767067