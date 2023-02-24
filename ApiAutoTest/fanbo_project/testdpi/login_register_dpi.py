# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：login_register_dpi.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/1/18 
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
from db.FrogSSHMysqlHandle import MysqlHandle
import re
# pip install faker-e164
from faker import Faker
from faker_e164.providers import E164Provider
logger = Loggers()

class LoginRegister:

    @staticmethod
    def send_msg_register(user_name_fb, area_code):
        url = frog["host"] + "/growAlong/v1/api/common/sendSmsV3"
        print("send_msg_url:{}".format(url))
        header = FrogHeader.get_header()
        print(header)
        data = {"smsCode":"",
            "areaCode": area_code,  # 区号
            "code": "register",
            "type": "mobile",
            "userName": user_name_fb  # 登陆手机号
        }
        # frog_req = FrogRequest()
        send_msg_res = frog_req.post(url, headers=header, json=data)
        print("send_msg:{}".format(send_msg_res))
        return send_msg_res

    @staticmethod
    def send_msg_login(user_name_fb, area_code):
        url = frog["host"] + "/growAlong/v1/api/common/sendSmsV3"
        print("send_msg_url:{}".format(url))
        header = FrogHeader.get_header()
        print(header)
        data = {
            "areaCode": area_code,  # 区号
            "code": "login",
            "type": "mobile",
            "userName": user_name_fb  # 登陆手机号
        }
        # frog_req = FrogRequest()
        send_msg_res = frog_req.post(url, headers=header, json=data)
        print("send_msg:{}".format(send_msg_res))
        return send_msg_res

    @staticmethod
    def register_fb(area_code, user_name_fb, sms_code, eName):
        #
        # send_msg_res = LoginRegister.send_msg_register(area_code=area_code)
        # print("return value:{}".format(send_msg_res))
        url = "https://test.frogcool.com/growAlong/v1/api/common/validSmsCode"
        print("send_msg_url:{}".format(url))
        header = FrogHeader.get_header()
        print(header)

        # con = MysqlHandle()
        # data = con.select("SELECT sms_code FROM send_sms_mail_rec WHERE user_numbers = {} AND area_code = {} ORDER BY id DESC LIMIT 1".format(user_name_fb, area_code), True)
        # sms_code = data[0]
        data = {
            "eName": eName,
            "type": "mobile",
            "areaCode": area_code,  # 区号
            "code": "register",
            "smsCode": sms_code,  # 验证码
            "userName": user_name_fb  # 登陆手机号
        }
        # frog_req = FrogRequest()
        res = frog_req.post(url, headers=header, json=data)
        logger.info("登陆返回: {}".format(res))
        # print("登陆返回: {}".format(res))
        return res
    @staticmethod
    def login_fb(area_code, user_name_fb):


        # send_msg_res = LoginRegister.send_msg_login(user_name_id=user_name_fb, area_code=area_code)
        # print("return value:{}".format(send_msg_res))
        url = "https://test.frogcool.com/growAlong/v1/api/common/validSmsCode"
        print("send_msg_url:{}".format(url))
        header = FrogHeader.get_header()
        print(header)
        con = MysqlHandle()
        data = con.select("SELECT sms_code FROM send_sms_mail_rec WHERE user_numbers = {} AND area_code = {} ORDER BY id DESC LIMIT 1".format(user_name_fb, area_code), True)
        sms_code = data[0]
        data = {
            "areaCode": area_code,  # 区号
            "code": "login",
            "smsCode": sms_code,  # 验证码
             "type": "mobile",
            "userName": user_name_fb  # 登陆手机号
        }
        # frog_req = FrogRequest()
        res = frog_req.post(url, headers=header, json=data)
        logger.info("登陆返回: {}".format(res))
        # print("登陆返回: {}".format(res))
        return res

    @staticmethod
    def smsCodeDb(user_name_fb, area_code):
        con = MysqlHandle()
        data = con.select("SELECT sms_code FROM send_sms_mail_rec WHERE user_numbers = {} AND area_code = {} ORDER BY id DESC LIMIT 1".format(user_name_fb, area_code), True)
        if data is None:
            return None
        else:
            sms_code = data[0]
            return sms_code

    @staticmethod
    def delUserInfoDb(user_name_fb, area_code):
        con = MysqlHandle()
        data = con.delete("DELETE FROM user_info WHERE telphone = {} AND areaCode = {} ORDER BY id DESC LIMIT 1".format(user_name_fb, area_code))
        return data