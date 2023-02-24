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
from testcases.FrogLogin import login_z
from config.FrogConf import UserName
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['metab']['personalVideo']

class TestPersonalvideo:
    def test_getUserVideoRepeatedlyList(self, login_z):
        """重复播放视频列表接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserVideoRepeatedlyListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getUserVideoRepeatedlyListApi']
        data = {
            "videoId": 75083751
        }
        logger.info("重复播放视频列表接口")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getUserVideoRepeatedlyList:{}".format(res))
        assert res['code'] == 200

    def test_getUserNewsVlogVideoUnreadList(self, login_z):
        """获取有未读视频用户播放列表接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserNewsVlogVideoUnreadListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getUserNewsVlogVideoUnreadListApi']
        logger.info("获取有未读视频用户播放列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getUserNewsVlogVideoUnreadList:{}".format(res))
        assert res['code'] == 200

    def test_getUserNewsVlogVideoReadList(self, login_z):
        """获取已读视频用户动态播放列表接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserNewsVlogVideoReadListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getUserNewsVlogVideoReadListApi']
        logger.info("获取已读视频用户动态播放列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getUserNewsVlogVideoReadList:{}".format(res))
        assert res['code'] == 200

    def test_saveNewsVlogVideoRead(self, login_z):
        """设置用户好友动态用户已读接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['saveNewsVlogVideoReadApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['saveNewsVlogVideoReadApi']
        logger.info("设置用户好友动态用户已读接口")
        res = frog_req.post(url, headers=header)
        logger.info("saveNewsVlogVideoRead:{}".format(res))
        assert res['code'] == 200

    def test_getBootAnimationFlag(self, login_z):
        """新用户引导动画状态获取接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getBootAnimationFlagApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getBootAnimationFlagApi']
        logger.info("新用户引导动画状态获取接口")
        res = frog_req.post(url, headers=header)
        logger.info("getBootAnimationFlag:{}".format(res))
        assert res['code'] == 200

    def test_saveBootAnimationFlag(self, login_z):
        """新用户引导动画状态设置接口"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['saveBootAnimationFlagApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['saveBootAnimationFlagApi']
        logger.info("新用户引导动画状态设置接口")
        res = frog_req.post(url, headers=header)
        logger.info("saveBootAnimationFlag:{}".format(res))
        assert res['code'] == 200


    #该接口已不使用
    # def test_createDesktopComponents(self, login_z):or
    #     """ios小组件"""
    #     # dataObj = login_z["body"]["data"]["dataObject"]
    #     # sId = dataObj["sId"]
    #     # id = login_z["body"]["userId"]
    #     # token = dataObj["token"]
    #     # api = yml['createDesktopComponentsApi']
    #     # header = FrogHeader.get_header()
    #     # header["sid"] = sId
    #     # header["userId"] = "{}".format(id)
    #     # header["token"] = token
    #     header = login_z
    #     url = frog["host"] + yml['createDesktopComponentsApi']
    #     logger.info("ios小组件")
    #     res = frog_req.post(url, headers=header)
    #     logger.info("createDesktopComponents:{}".format(res))
    #     assert res['code'] == 200

    def test_getUserVlogCreateVideoList(self, login_z):
        """合成视频列表"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserVlogCreateVideoListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getUserVlogCreateVideoListApi']
        data = {
            "page": 2,
            "pageSize": 30,
            "hasMore": 'true'
        }
        logger.info("合成视频列表")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getUserVlogCreateVideoList:{}".format(res))
        assert res['code'] == 200

    def test_getCorrelationSubCreateVideoList(self, login_z):
        """合成子视频列表"""
        # dataObj = login_z["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_z["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getCorrelationSubCreateVideoListApi']
        # header = FrogHeader.get_header()
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_z
        url = frog["host"] + yml['getCorrelationSubCreateVideoListApi']
        data = {
            "videoId": "23606211"
        }
        logger.info("合成子视频列表")
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getCorrelationSubCreateVideoList:{}".format(res))
        assert res['code'] == 200
