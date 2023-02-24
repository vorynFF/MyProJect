# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_metab.py
@IDE     ：PyCharm
@Author  ：fanbo
@Date    ：2021/12/2
"""

import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
import json
import time
from common.FrogHeader import FrogHeader
from db.FrogSSHMysqlHandle import MysqlHandle
from testcases import FrogLogin
from utils.Logger import Logger
from utils.AESCipher import AESCipher
from utils.Loggers import Loggers
from testcases.FrogLogin import login_fb,login_whb,login_sls
from config.FrogConf import UserName
import allure

from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['metab']['meta']
con = MysqlHandle()

class TestMeTab:
    def test_getUserVlogVideoList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserVlogVideoListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        # print("header:{}".format(header))
        header = login_fb
        id = header['userId']
        url = frog["host"] + yml['getUserVlogVideoListApi']
        logger.info("获取个人主页视频列表接口")
        friendUserId = 46555087
        data = "{\"friendUserId\":%s}" % friendUserId

        res_me = frog_req.post(url, headers=header)  # 自己主页视频列表不用传参数
        res_user = frog_req.post(url, headers=header, data=data)  # 他人主页视频列表需要传参
        logger.info("MyVlogVideoList:{}".format(res_me))
        assert res_me['code'] == 200

        logger.info("UserVlogVideoList:{}".format(res_user))
        assert res_user['code'] == 200
        key = "rC5bF3tR7mP1rX1k"
        aescipher = AESCipher(key)
        myVideoListData = aescipher.decrypt(res_me['body']['data'])
        logger.info("解密后myVideoListData:{}".format(myVideoListData))
        myVideoDataDict = json.loads(myVideoListData)

        userVideoListData = aescipher.decrypt(res_user['body']['data'])
        logger.info("解密后userVideoListData:{}".format(userVideoListData))
        userVideoDataDict = json.loads(userVideoListData)
        assert len(myVideoDataDict) > 0
        assert len(userVideoDataDict) > 0
        myVideoList = myVideoDataDict['findRespVoList']
        assert myVideoList[0]['videoUserId'] == str(id)
        userVideoList = userVideoDataDict['findRespVoList']
        assert userVideoList[0]['videoUserId'] == str(friendUserId)
        my_video_list = None
        user_video_list = None
        for myVideo in myVideoList:
            if myVideo['videoId'] == "54022121":
                my_video_list = myVideo
                break
        for userVideo in userVideoList:
            if userVideo['videoId'] == "97837202":
                user_video_list = userVideo
                break
        assert my_video_list is not None
        assert user_video_list is not None
        my_video_url = my_video_list['videoUrl']
        assert my_video_url == "https://dx265v3f1t09x.cloudfront.net/public/frog/android/video/TXVideo_163783778283901ae012474684b1981a4a18c810bdd6f1637582030341.mp4"

        user_video_EName = user_video_list['videoUserEName']
        assert user_video_EName == '15800000055'

    def test_getUser(self, login_fb):
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
        url = frog["host"] + yml['getUserApi']
        logger.info("获取个人主页信息接口")
        res = frog_req.post(url, headers=header)
        logger.info("getUser:{}".format(res))
        assert res['code'] == 200
        userInfo = res['body']['data']
        assert len(userInfo) > 0
        assert userInfo['frogId'].replace(" ", "") == "0515764540"
        assert userInfo['telphone'] == FrogLogin.user_name_fb54

    def test_getFriendUser(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getFriendUserApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getFriendUserApi']
        logger.info("获取他人主页信息接口")
        data = {"friendUserId": 33769113}
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getFriendUser:{}".format(res))
        assert res['code'] == 200
        friendUserInfo = res['body']['data']
        assert len(friendUserInfo) > 0

        assert friendUserInfo['eName'] == "Kkkm"
        assert friendUserInfo['addFriendStatus'] == "2"

    def test_getIndexMsgRecListV2(self, login_fb):
        # 个人主页LIKE,ATTITUDE列表接口和FRIENDS待同意好友申请列表接口
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getIndexMsgRecListV2Api']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['getIndexMsgRecListV2Api']
        logger.info("个人主页点赞,礼物和申请好友列表接口")
        queryType = {"like": "vote_video",  # like列表
                     "gift": "gift",  # 礼物列表
                     "friend": "apply_add_friend"}  # 待接受好友申请列表
        data_like = "{\"queryType\":\"%s\"}" % queryType['like']
        data_gift = "{\"queryType\":\"%s\"}" % queryType['gift']
        data_friend = "{\"queryType\":\"%s\"}" % queryType['friend']

        res_like = frog_req.post(url, headers=header, data=data_like)
        res_gift = frog_req.post(url, headers=header, data=data_gift)
        res_friend = frog_req.post(url, headers=header, data=data_friend)
        logger.info("getLikeList:{}".format(res_like))
        logger.info("getGiftList:{}".format(res_gift))
        logger.info("getApplyAddFriendList:{}".format(res_friend))
        assert res_friend['code'] == 200
        assert res_like['code'] == 200
        assert res_gift['code'] == 200

        assert res_like['body']['userId'] == id
        assert res_gift['body']['userId'] == id
        assert res_friend['body']['userId'] == id
        indexLikeList = res_like['body']['data']['indexMsgRecList']
        indexGiftList = res_gift['body']['data']['indexMsgRecList']
        indexFriendList = res_friend['body']['data']['indexMsgRecList']

        assert len(indexLikeList) > 0
        assert len(indexGiftList) > 0
        assert len(indexFriendList) > 0
        giftList = None
        likeList = None
        friendList = None
        for like_list in indexLikeList:
            if like_list['eName'] == "Kkkm":
                likeList = like_list
                break

        for gift_list in indexGiftList:
            if gift_list['eName'] == "Kkkm":
                giftList = gift_list
                break
        for friend_list in indexFriendList:
            if friend_list['eName'] == "test0058":
                friendList = friend_list
                break
        assert likeList is not None
        assert giftList is not None
        assert friendList is not None
        assert likeList['friendUserId'] == 33769113
        assert giftList['friendUserId'] == 33769113
        assert friendList['friendUserId'] == 31952767

    def test_getFriendList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getFriendListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb

        print("header:{}".format(header))
        url = frog["host"] + yml['getFriendListApi']
        logger.info("Friends好友列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getFriendList:{}".format(res))
        assert res['code'] == 200
        friendList = res['body']['data']
        assert len(friendList) > 0
        friend_list = None
        for friend in friendList:
            if friend['eName'] == "Kkkm":
                friend_list = friend
                break
        assert friend_list is not None
        key = "rC5bF3tR7mP1rX1k"
        aescipher = AESCipher(key)
        friend_user_id = aescipher.decrypt(friend_list['friendUserId'])
        assert friend_user_id == "33769113"

    def test_getUserAuthCardsList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getUserAuthCardsListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getUserAuthCardsListApi']
        logger.info("个人主页card信息接口")
        res = frog_req.post(url, headers=header)
        logger.info("getUserAuthCardsList:{}".format(res))
        assert res['code'] == 200

        cardsList = res['body']['data']['cardsList']
        assert len(cardsList) > 0
        card_info = None
        for card in cardsList:
            if card['id'] == 5000066:
                card_info = card
                break

        assert card_info is not None
        assert card_info['cardsUserName'] == "kkkkkl"

    def test_getPurchaseList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getPurchaseListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getPurchaseListApi']
        data_ios = """{"queryType":"cybermoney_en_iOS"}"""
        data_and = """{"queryType":"cybermoney_en_Android"}"""

        logger.info("个人主页swim ring信息接口")
        res_ios = frog_req.post(url, headers=header, data=data_ios)
        logger.info("iosGetPurchaseList:{}".format(res_ios))
        assert res_ios['code'] == 200
        coursePackageModelList = res_ios['body']['data']['coursePackageModelList']
        assert len(coursePackageModelList) > 0
        mode_list = None
        for mode in coursePackageModelList:
            if mode['id'] == 15:
                mode_list = mode
                break
        assert mode_list is not None
        assert mode_list['packageIncluded']['proId'] == "frog.sring.79992"

    def test_getGiftInfoList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getGiftInfoListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getGiftInfoListApi']
        data = """{"queryType":"v1_gift"}"""
        logger.info("礼物商店接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("getGiftInfoList:{}".format(res))
        assert res['code'] == 200
        giftInfoList = res['body']['data']['giftInfoList']
        assert len(giftInfoList) > 0
        giftInfo_List = None
        for giftInfo in giftInfoList:
            if giftInfo['id'] == 36:
                giftInfo_List = giftInfo
                break
        assert giftInfo_List is not None
        assert giftInfo_List['giftEName'] == "cool"
        return res

    def test_buyGifts(self, login_fb):
        res_r = TestMeTab.test_getGiftInfoList(self, login_fb)
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['buyGiftsApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['buyGiftsApi']
        data = """{"giftId":"15","giftSize":"1"}"""
        logger.info("购买礼物接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("buyGifts:{}".format(res))
        assert res['code'] == 200
        assert len(res['body']['data']) > 0
        balanceSumF = res_r['body']['data']['balanceSum']
        balanceSumB = res['body']['data']['balanceSum']

        if res['body']['data']['buyFlag'] == "true":
            assert balanceSumB == balanceSumF - 2
        else:
            assert balanceSumB == balanceSumF

    def test_getToolkitTxt(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getToolkitTxtApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['getToolkitTxtApi']
        logger.info("自动回复列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getToolkitTxt:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        return res

    def test_saveToolkitTxt(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['saveToolkitTxtApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        # print("header:{}".format(header))
        header = login_fb
        url = frog["host"] + yml['saveToolkitTxtApi']
        logger.info("保存自动回复列表接口")
        data_bomb = """{"bombTxt": "pythontestbomb", "id": "0", "toolkitType": "faceTxt"}"""
        data = """{"id": "0", "friendTxt": "pythontest", "toolkitType": "faceTxt"}"""
        data_like = """{"likeTxt": "pythontestlike", "id": "0", "toolkitType": "faceTxt"}"""
        data_gift = """{"giftTxt": "pythontestgift", "id": "0", "toolkitType": "faceTxt"}"""
        res = frog_req.post(url, headers=header, data=data)
        res_bomb = frog_req.post(url, headers=header, data=data_bomb)
        res_like = frog_req.post(url, headers=header, data=data_like)
        res_gift = frog_req.post(url, headers=header, data=data_gift)
        logger.info("saveToolkitTxt:{}".format(res))
        logger.info("saveBombToolkitTxt:{}".format(res_bomb))
        logger.info("saveLikeToolkitTxt:{}".format(res_like))
        logger.info("saveGiftToolkitTxt:{}".format(res_gift))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0

        assert res_bomb['code'] == 200
        assert res_bomb['body']['state']['code'] == 0

        assert res_like['code'] == 200
        assert res_like['body']['state']['code'] == 0

        assert res_gift['code'] == 200
        assert res_gift['body']['state']['code'] == 0
        res_list = TestMeTab.test_getToolkitTxt(self, login_fb)
        assert res_list['body']['data']['giftTxt'] == "pythontestgift"
        assert res_list['body']['data']['bombTxt'] == "pythontestbomb"
        assert res_list['body']['data']['likeTxt'] == "pythontestlike"
        assert res_list['body']['data']['friendTxt'] == "pythontest"

    def test_getIndexMsgRecListV2(self, login_sls):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getIndexMsgRecListV2Api']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_sls
        print("header:{}".format(header))
        url = frog["host"] + yml['getIndexMsgRecListV2Api']
        data = """{"queryType":"gift"}"""
        logger.info("收到的礼物列表接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("getIndexMsgRecListV2:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        indexMsgRecList = res['body']['data']['indexMsgRecList']
        assert len(indexMsgRecList) > 0
        index_list = []
        # eNameList = []

        for index in indexMsgRecList:
            if index['friendUserId'] == 43211195:
                index_list.append(index['eName'])
                break
        print(index_list)
        assert index_list is not None
        assert "wuhaibo" in index_list

    def test_sendExpression(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['sendExpressionApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        print("header:{}".format(header))
        url = frog["host"] + yml['sendExpressionApi']
        data = """{"recType": "user_thank", "friendUserId": "33769113", "type": "user_thank", "recId": ""}"""
        logger.info("感谢送礼物接口")
        res = frog_req.post(url, headers=header, data=data)
        logger.info("sendExpression:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0

    #  用户英文名搜索接口-tiktok,ins
    def test_getUserENameList(self, login_whb):
        url = frog["host"] + yml['getUserENameListApi']
        header = login_whb
        data = {"selectValue": "ww"}
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getUserENameList response: {}".format(res))
        assert res['body']['state']['msg'] == 'get successful;get successful'
        assert res




if __name__ == '__main__':
    pytest.main('-q test_metab.py')
