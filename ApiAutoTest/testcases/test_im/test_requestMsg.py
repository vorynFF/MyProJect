# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：test_requestMsg.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/12/14 
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
import common.FrogSSHRedis as frogRedis
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.YmlUtil import ymlUtil

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['im']['requestMsg']


class TestRequestMsg:
    def test_getRequestMsgList(self, login_whb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getRequestMsgListApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_whb
        id = int(header['userId'])
        print("header:{}".format(header))
        url = frog["host"] + yml['getRequestMsgListApi']
        logger.info("假聊天消息列表接口")
        res = frog_req.post(url, headers=header)
        logger.info("getRequestMsgList:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        findRespVoList = res['body']['data']['findRespVoList']
        print("findRespVoList: " + str(findRespVoList))
        assert len(findRespVoList) > 0
        user_id_list = []

        sql = "SELECT " \
              "     id msg_id,sender_user_id,recipient_user_id,user_id,head_img_url,e_name,c_name,social,create_time,msg_read_status " \
              "FROM " \
              "     ((" \
              "SELECT" \
              "      req.id,sender_user_id,recipient_user_id,u.id user_id,u.head_img_url,u.e_name,u.c_name,u.social,req.create_time,req.msg_read_status" \
              " FROM " \
              "     request_msg_rec req,user_info u " \
              "WHERE u.STATUS='1' AND req.del_flag !=1 AND u.id=req.sender_user_id AND req.recipient_user_id={} " \
              "ORDER BY create_time DESC,req.id DESC LIMIT 999999999) " \
              "UNION ALL " \
              "     (SELECT " \
              "         req.id,sender_user_id,recipient_user_id,u.id user_id,u.head_img_url,u.e_name,u.c_name,u.social,req.create_time,1 " \
              "      FROM " \
              "         request_msg_rec req,user_info u " \
              "     WHERE " \
              "         u.STATUS='1' AND req.del_flag !=1 AND u.id=req.recipient_user_id AND req.sender_user_id={} " \
              "     ORDER BY create_time DESC,req.id DESC LIMIT 999999999)) r " \
              "WHERE 1=1 GROUP BY user_id ORDER BY create_time DESC,msg_id DESC".format(id,id)
        data = con.select(sql, one=True)
        for i in findRespVoList:
            user_id_list.append(i['userId'])
        assert data[3] in user_id_list

    def test_getRequestFriendMsgList(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        #
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        get_friendUserId_sql = "select sender_user_id, recipient_user_id from request_msg_rec where (sender_user_id = {} or recipient_user_id = {}) and msg_type != 'txtTip' and del_flag = 0;".format(
            id, id)
        data = con.select(get_friendUserId_sql, one=True)
        print(data)
        assert data is not None  # 校验数据库查询是否为空
        if data[0] == id:
            friendUserId = data[1]
        else:
            friendUserId = data[0]
        print("header:{}".format(header))
        id_data = {"friendUserId": "{}".format(friendUserId)}
        url = frog["host"] + yml['getRequestFriendMsgListApi']
        logger.info("request消息单个聊天记录列表接口")
        res = frog_req.post(url, headers=header, json=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        findRespVoList = res['body']['data']['pageListResp']['findRespVoList']
        sql = "select count(id) from request_msg_rec where (sender_user_id = {} and recipient_user_id = {}) or (sender_user_id = {} and recipient_user_id = {});".format(
            id, friendUserId, friendUserId, id)
        data1 = con.select(sql, one=True)
        assert res['body']['data']['pageListResp']['toTalSize'] == data1[0]

    def test_getMsgChatStatus(self, login_fb):
        # dataObj = login_fb["body"]["data"]["dataObject"]
        # sId = dataObj["sId"]
        # id = login_fb["body"]["userId"]
        # token = dataObj["token"]
        # api = yml['getMsgChatStatusApi']
        # header = FrogHeader.get_header()
        # # 添加header数据
        # header["sid"] = sId
        # header["userId"] = "{}".format(id)
        # header["token"] = token
        header = login_fb
        id = int(header['userId'])
        print("header:{}".format(header))
        id_data = {"friendUserId": "78431590"}
        url = frog["host"] + yml['getMsgChatStatusApi']
        logger.info("获取是否可真聊天接口")
        res = frog_req.post(url, headers=header, json=id_data)
        logger.info("res:{}".format(res))
        assert res['code'] == 200
        assert res['body']['state']['code'] == 0
        assert res['body']['userId'] == id
        chatStatus = res["body"]["data"]["chatStatus"]
        assert chatStatus == "decline"

    def test_getAccessToken(self, login_whb):
        header = login_whb
        print("header:{}".format(header))
        url = frog["host"] + yml['getAccessTokenApi']
        logger.info("获取AccessToken")
        res = frog_req.post(url, headers=header)
        logger.info("getAccessTokenApi response:{}".format(res))
        assert res['body']['data'] is not None
