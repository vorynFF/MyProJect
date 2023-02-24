# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_pondNominated.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/11/26 
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
from testcases.FrogLogin import login_fb, login_whb
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['pond']['pondNominated']


class TestPondNominated:
    def test_getUserNominatedList(self, login_fb):  # 获取pond nominated列表接口
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getUserNominatedListApi']
        logger.info("pond nominated列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("PondNominatedList:{}".format(res))
        assert res['code'] == 200
        nominatedList = res['body']['data']['findRespVoList']
        assert len(nominatedList) > 0
        sponsor_userid = None
        for sponsor in nominatedList:
            if sponsor['sponsorUserId'] == 62867000:
                sponsor_userid = sponsor
                break
        assert sponsor_userid is not None
        video_id = sponsor_userid['videoId']
        assert video_id == 21195650

    def test_getFriendFeedList(self, login_fb):  # 好友动态列表接口
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getFriendFeedListApi']
        logger.info("好友动态列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("FriendSupList:{}".format(res))
        assert res['code'] == 200

        indexMsgList = res['body']['data']['indexMsgList']
        assert len(indexMsgList) > 0

        friends_feed = None
        for friend in indexMsgList:
            if friend['dataDetail']['userInfo']['eName'] == '85858585':
                friends_feed = friend
                break
        assert friends_feed is not None
        user_id = friends_feed['dataDetail']['userInfo']['userId']
        assert user_id == 85484422

    def test_quickAddList(self, login_whb):  # 获取推荐好友用户列表接口
        header = login_whb
        print("header:{}".format(header))
        url = frog["host"] + yml['quickAddListApi']
        logger.info("获取推荐好友用户列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("QuickAddList:{}".format(res))
        assert res['code'] == 200

        quickAddList = res['body']['data']['findRespVoList']
        assert quickAddList != []

    def test_getPondTagVideoList(self, login_fb):  # 话题视频列表接口
        header = login_fb
        print("header:{}".format(header))
        data = "{\"tagValue\":\"2021\"}"  # tagId和tagValue必传其一
        url = frog["host"] + yml['getPondTagVideoListApi']
        logger.info("话题视频列表接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("PondTagVideoList:{}".format(res))
        assert res['code'] == 200

        key = "rC5bF3tR7mP1rX1k"
        aescipher = AESCipher(key)

        videoData = aescipher.decrypt(res['body']['data'])
        logger.info("解密后data:{}".format(videoData))
        videoDataDict = json.loads(videoData)

        assert len(videoDataDict) > 0

        videoList = videoDataDict['findRespVoList']
        assert videoList[0]['tagId'] == 477
        video_list = None
        for video in videoList:
            if video['videoUserEName'] == "Nicole":
                video_list = video
                break
        assert video_list is not None
        assert video_list['videoUserId'] == "90501132"

    def test_getPondVideoList(self, login_fb):
        header = login_fb
        print("header:{}".format(header))
        # data = "{\"tagValue\":\"2021\"}"        # tagId和tagValue必传其一
        url = frog["host"] + yml['getPondVideoListApi']
        logger.info("池塘视频列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("PondTagVideoList:{}".format(res))
        assert res['code'] == 200
        key = "rC5bF3tR7mP1rX1k"
        aescipher = AESCipher(key)

        videoData = aescipher.decrypt(res['body']['data'])
        logger.info("解密后data:{}".format(videoData))


if __name__ == '__main__':
    pytest.main('-q test_pondNominated.py')
