# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：login.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/20 7:13 下午 
'''
import pytest
from common.FrogRequest import frog_req
from config.FrogConf import frog
import hashlib
import json
import time
from common.FrogHeader import FrogHeader
from utils.Loggers import Loggers
from config.FrogConf import UserName
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['login']

userName = "19965225020"  # 19965225020
user_name_fb54 = UserName['user_name_fb54']
# user_name_fb54 = "15800000001"
user_name_fb55 = UserName['user_name_fb55']


# user_name_zzz = UserName['user_name_zzz']
# userName = "13721089003"


# @pytest.fixture(scope="module")
def send_msg(user_name_id):
    url = frog["host"] + yml["sendSmsV3Api"]
    # print("send_msg_url:{}".format(url))
    header = FrogHeader.get_header()
    # print(header)
    data = {
        "areaCode": "86",  # 区号
        "code": "login",
        "type": "mobile",
        "userName": user_name_id  # 登陆手机号
    }
    # frog_req = FrogRequest()
    send_msg_res = frog_req.post(url, headers=header, json=data)
    # print("send_msg:{}".format(send_msg_res))
    return send_msg_res


def frog_login(user_name_id):
    send_msg_res = send_msg(user_name_id)
    print("send_msg_res response: {}".format(str(send_msg_res)))
    # print("return value:{}".format(send_msg_res))
    assert send_msg_res["code"] == 200
    url = frog["host"] + yml["validSmsCodeApi"]
    # id = "1636022967658"
    key = "846d2cb0c7f09c3ae582c421696d308c"
    # timestamp = "1636022967658"
    timestamp = str(int(round(time.time() * 1000)))

    id = timestamp
    m = hashlib.md5()
    union_str = id + ":" + key + ":" + timestamp
    m.update(union_str.encode(encoding="utf-8"))
    str_md5 = m.hexdigest()
    # print(str_md5)
    header = {
        "caller": "app",
        "ex": "",
        "os": "15.0.2",
        "platform": "iOS",
        "ver": "1.8.84",
        "encrypt": "md5",
        "etag": "qqq",  # 不为空，任意值，与其他接口请求头一致
        "id": id,  # 任意数字
        "sign": str_md5,  # id+key+timestamp加密处理
        "timestamp": timestamp,
        "language": "en",
        "content-type": "application/json"
    }
    data = {
        "areaCode": "86",  # 区号
        "code": "login",
        "smsCode": "1111",  # 验证码
        "type": "mobile",
        "userName": user_name_id  # 登陆手机号
    }
    # frog_req = FrogRequest()
    res = frog_req.post(url, headers=header, json=data)
    logger.info("登陆返回: {}".format(res))
    # print("登陆返回: {}".format(res))
    return res


def frog_header(user_name_id):
    res = frog_login(user_name_id)
    logger.info("登陆返回: {}".format(res))
    dataObj = res["body"]["data"]["dataObject"]
    sId = dataObj["sId"]
    id = res["body"]["userId"]
    token = dataObj["token"]
    header = FrogHeader.get_header()
    # 添加header数据
    header["sid"] = sId
    header["userId"] = "{}".format(id)
    header["token"] = token
    return header


@pytest.fixture(scope="module")
def login():
    header = frog_header(userName)
    return header


@pytest.fixture(scope="module")
def login_fb():
    header = frog_header(user_name_fb54)
    return header


@pytest.fixture(scope="module")
def login_whb():
    user_name = ymlUtil().get["frog"]['user']['mobile']['wuhaibo']
    header = frog_header(user_name)
    return header


@pytest.fixture(scope="module")
def login_yh():
    user_name_yh = "13353337992"
    header = frog_header(user_name_yh)
    return header


@pytest.fixture(scope="module")
def login_yh_2():
    user_name_yh = "18716010137"
    header = frog_header(user_name_yh)
    return header


@pytest.fixture(scope="module")
def login_fb55():
    user_name_fb = "15800000054"
    header = frog_header(user_name_fb)
    return header


@pytest.fixture(scope="module")
def login_smy():
    user_name_smy = "18822113062"
    header = frog_header(user_name_smy)
    return header


@pytest.fixture(scope="module")
def login_z():
    """登陆账号"""
    userName_z = "18232126335"
    header = frog_header(userName_z)
    return header


@pytest.fixture(scope="module")
def login_sls():
    """登陆账号"""
    user_name_sls = "17700000777"
    header = frog_header(user_name_sls)
    return header


@pytest.fixture(scope="module")
def login_response():
    response = frog_login(ymlUtil().get["frog"]['user']['mobile']['wuhaibo2'])
    return response


if __name__ == "__main__":
    pass
