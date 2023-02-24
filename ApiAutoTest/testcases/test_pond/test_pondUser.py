"""
@Project ：FrogApiAutoTest
@File    ：test_whatsUp.py
@IDE     ：PyCharm
@Author  ：yuhang
@Date    ：2021/12/9 下午5:11
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
from testcases.FrogLogin import login_fb,login_yh,login_whb

import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()

yml = ymlUtil().get["frog"]['api']['pond']['pondUser']

class TestPondTest:

    def test_getVideoUserInfo(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getVideoUserInfoApi'] # ?videoUserId=67864402"
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        json_data = {"videoUserId":"67864402"}
        print("header:{}".format(header))
        url = frog["host"] + yml['getVideoUserInfoApi']
        logger.info("获取视频页面，用户信息接口")
        res = frog_req.post(url, headers=header, json=json_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        # mutualFriendSize = res["body"]["data"]["mutualFriend"]["mutualFriendSize"]
        # assert mutualFriendSize >= 1
        bestFriendOfList = res["body"]["data"]["mutualFriend"]["bestFriendOfList"]
        bfList = []
        for bf in bestFriendOfList:
            bfList.append(bf["bestFriendName"])
        print(bfList)
        assert 'restrictions' in bfList

    def test_getUserPondTagVideoList(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserPondTagVideoListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        tag_data = "{\"tagValue\":\"2021\", \"videoId\":\"83150269\", \"friendUserId\":\"32330898\"}"  # tagId和tagValue必传其一
        url = frog["host"] + yml['getUserPondTagVideoListApi']
        logger.info("获取当前用户池塘主题视频播放列表")
        res = frog_req.post(url, headers=header, data=tag_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        res_data = res["body"]["data"]
        key = "rC5bF3tR7mP1rX1k"  # 对data解密
        aes_cipher = AESCipher(key)
        pondData = aes_cipher.decrypt(res_data)
        videoDataDict = json.loads(pondData)  # 转换为字典
        assert videoDataDict["findRespVoList"][0]["tagValue"] == "2021"

    def test_getFriendStatusInfo(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getFriendStatusInfoApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        id_data = "{\"friendUserId\":\"62867000\"}"
        url = frog["host"] + yml['getFriendStatusInfoApi']
        logger.info("获取好友状态信息接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        addFriendStatus = res["body"]["data"]["addFriendStatus"]
        assert addFriendStatus == "2"  # 2表示已经是好友

    def test_getFriendVlogList(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getFriendVlogListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        id_data = "{\"friendUserId\":\"62867000\"}"
        url = frog["host"] + yml['getFriendVlogListApi']
        logger.info("好友日常视频连播视频列表接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        vlogList = res["body"]["data"]["vlogList"]
        assert len(vlogList) > 1

    def test_oauthLogin(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['oauthLoginApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        print("header:{}".format(header))
        url = frog["host"] + yml['oauthLoginApi']
        logger.info("一键登录接口")
        res = frog_req.post(url, headers=header)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        msg = res["body"]["state"]["msg"]
        assert msg == "Login Successful;Login Successful"

    def test_getVideoPlayInfo(self, login_yh):
        # dataObj = login_yh["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_yh["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getVideoPlayInfoApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_yh
        id_data = "{\"videoId\":\"45724410\",\"friendUserId\":\"48002321\"}"
        print("header:{}".format(header))
        url = frog["host"] + yml['getVideoPlayInfoApi']
        logger.info("获取视频播放页面信息接口")
        res = frog_req.post(url, headers=header, data=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        followStatus = res["body"]["data"]["followStatus"]
        assert followStatus == "2"
        videoInfo = res["body"]["data"]["videoInfo"]
        assert videoInfo["videoType"] == "friend"

    def test_helpVideo(self,login_whb):
        header = login_whb
        url = frog["host"] + yml['getHelpVideoApi']
        logger.info("获取用户帮助视频接口")
        res = frog_req.post(url, headers=header)
        logger.info("getHelpVideo response:{}".format(res))
        assert res['body']['state']['msg']  == 'get successful;get successful'
        assert len(res['body']['data']) != 0


if __name__ == '__main__':
    pytest.main('-q test_pondUser.py')
