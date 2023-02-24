# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_sendToFriendList.py
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
yml = ymlUtil().get["frog"]['api']['friends']['sendToFriendList']

class TestSendToFriendList:
    def test_sendToFriendList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['sendToFriendListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['sendToFriendListApi']
        logger.info("获取sendTo列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("sendToFriendList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        friendUserMsgList = res['body']['data']['friendUserMsgList']
        friendUserList = res['body']['data']['friendUserList']
        friendUserMsgListKey = "api:user:{}:friendNewIMMsgUserList".format(id)
        friendUserListKey = "api:user:{}:getFriendUserList:data".format(id)
        friend_userid_list = []
        friend_msg_userid_list = []
        assert len(friendUserList) > 0
        if len(friendUserList) > 0:
            redis_str_res = frogRedis.str_get(friendUserListKey)
            if redis_str_res is not None:
                redis_js_res = json.loads(redis_str_res)
                for i in redis_js_res:
                    friend_userid_list.append(i['friendUserId'])
                assert friendUserList[0]['friendUserId'] in friend_userid_list
            else:
                follow_info_sql = "select to_user_id from follow_info where rom_user_id = {} and both_status = 1 and del_status = 0;".format(
                    id)
                data = con.select(follow_info_sql, one=True)
                friend_user_id = data[0]
                friend_info_sql = "select e_name from user_info where id = {}".format(friend_user_id)
                data1 = con.select(friend_info_sql, one=True)
                friend_ename = data1[0]
                for i in friendUserList:
                    if i['friendUserId'] == friend_user_id:
                        assert i['eName'] == friend_ename



        assert len(friendUserMsgList) > 0

        if len(friendUserMsgList) > 0:
            redis_zset_res = frogRedis.zset_getall(friendUserMsgListKey)
            for i in redis_zset_res:
                friend_msg_userid_list.append(int(i[0]))
            sql = "select user_id from user_shake_rec where  friend_user_id = {} and del_flag = 0;".format(id)
            data2 = con.select(sql)
            for i in data2:
                friend_msg_userid_list.append(i[0])
            assert friendUserMsgList[0]['friendUserId'] in friend_msg_userid_list


        # friend_user_msg_list = None
        # friend_user_list = None
        #
        # for friendMsg in friendUserMsgList:
        #     if friendMsg['friendUserId'] == 33769113:
        #         friend_user_msg_list = friendMsg
        #         break
        # for friend in friendUserList:
        #     if friend['friendUserId'] == 46555087:
        #         friend_user_list = friend
        #         break
        # assert friend_user_list is not None
        # assert friend_user_msg_list is not None
        #
        # assert friend_user_msg_list['eName'] == "Kkkm"
        # assert friend_user_list['eName'] == "15800000055"

