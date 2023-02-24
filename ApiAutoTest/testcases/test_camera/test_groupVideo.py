# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_groupVideo.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/13 
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
from testcases.FrogLogin import login_fb
import allure
from testcases.redistest import RedisTest
from testcases.FrogLogin import login_fb55
import FrogSSHRedis
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['camera']['groupVideo']


class TestGroupVideo:
    def test_getGroupVideoMsgList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api =
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getGroupVideoMsgListApi']
        logger.info("获取合拍待处理列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getGroupVideoMsgList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == int(header['userId'])
        topList = res['body']['data']['topList']
        belowList = res['body']['data']['belowList']
        assert len(topList) > 0 or len(belowList) > 0
        if len(topList) > 0:
            rom = random.randint(0, len(topList)-1)
            sql = "select sponsor_user_id from video_multiple_rec where id = {};".format(topList[rom]['proId'])
            sql1 = "select video_id from video_multiple_sub_rec where production_id = {} and user_id = {};".format(
                topList[rom]['proId'], topList[rom]['sponsorUserId'])
            data = con.select(sql, one=True)
            data1 = con.select(sql1, one=True)
            assert topList[rom]['sponsorUserId'] == data[0]
            assert topList[rom]['videoId'] == data1[0]

        if len(belowList) > 0:
            rom = random.randint(0, len(belowList)-1)

            sql = "select sponsor_user_id from video_multiple_rec where id = {}".format(belowList[rom]['proId'])
            sql1 = "select video_id from video_multiple_sub_rec where production_id = {} and user_id = {};".format(
                belowList[rom]['proId'], belowList[rom]['sponsorUserId'])
            data = con.select(sql, one=True)
            data1 = con.select(sql1, one=True)
            assert belowList[rom]['sponsorUserId'] == data[0]
            assert belowList[rom]['videoId'] == data1[0]
        # for video in topList:
        #     if video['proId'] == 5551748:
        #         group_video = video
        #         break
        # assert group_video['videoId'] == 43673572

    def test_getGroupVideoInfo(self, login_fb):
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
        count_sql = "select count(production_id) from video_multiple_sub_rec where user_id = {};".format(id)
        count_data = con.select(count_sql, one=True)
        count_num = count_data[0]
        sql = "select production_id from video_multiple_sub_rec where user_id = {};".format(id)# 通过userid查询该用户下的合拍视频id
        db_data = con.select(sql)
        data = {"proId": db_data[random.randint(0, count_num-1)][0]}
        url = frog["host"] + yml['getGroupVideoInfoApi']
        logger.info("获取单个合拍任务信息接口")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getGroupVideoInfo:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        multipleInfoList = res['body']['data']['multipleInfoList']  # multipleInfoList返回合拍中单个视频信息，双人合拍list长度为2，四人合拍为4
        assert len(multipleInfoList) > 0
        rom = random.randint(0, len(multipleInfoList)-1)
        sql1 = "select video_id, user_id from video_multiple_sub_rec where production_id = {} and video_sn = {};".format(
            res['body']['data']['proId'], rom)
        data1 = con.select(sql1, one=True)
        print(data1)
        assert data1[0] == multipleInfoList[rom]['videoId']
        assert data1[1] == multipleInfoList[rom]['friendUserId']
        # if multipleInfoList[0]['videoId'] is not None:  # 校验list中videoId与数据库是否匹配，video_sn为返回的list顺序
        #     sql1 = "select video_id, user_id from video_multiple_sub_rec where production_id = {} and video_sn = 0;".format(res['body']['data']['proId'])
        #     data1 = con.select(sql1, one=True)
        #     assert data1[0] == multipleInfoList[0]['videoId']
        #     assert data1[1] == multipleInfoList[0]['friendUserId']
        # elif multipleInfoList[1]['videoId'] is not None:
        #     sql1 = "select video_id, user_id from video_multiple_sub_rec where production_id = {} and video_sn = 1".format(res['body']['data']['proId'])
        #     data1 = con.select(sql1, one=True)
        #     assert data1[0] == multipleInfoList[1]['videoId']
        #     assert data1[1] == multipleInfoList[1]['friendUserId']
        # elif multipleInfoList[2]['videoId'] is not None:
        #     sql1 = "select video_id, user_id from video_multiple_sub_rec where production_id = {} and video_sn = 2".format(res['body']['data']['proId'])
        #     data1 = con.select(sql1, one=True)
        #     assert data1[0] == multipleInfoList[2]['videoId']
        #     assert data1[1] == multipleInfoList[2]['friendUserId']
        # else:
        #     sql1 = "select video_id, user_id from video_multiple_sub_rec where production_id = {} and video_sn = 3".format(res['body']['data']['proId'])
        #     data1 = con.select(sql1, one=True)
        #     assert data1[0] == multipleInfoList[3]['videoId']
        #     assert data1[1] == multipleInfoList[3]['friendUserId']
        # assert len(multipleInfoList) > 0
        # video_info = None
        # for video in multipleInfoList:
        #     if video['videoId'] == 43673572:
        #         video_info = video
        #         break
        # assert video_info is not None
        # assert video_info['eName'] == "15800000055"


