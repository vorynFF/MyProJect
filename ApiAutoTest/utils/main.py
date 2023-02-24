import hashlib
import time
from ast import Str

import requests

from common.FrogHeader import FrogHeader
from common.FrogRequest import frog_req
from config.FrogConf import frog
from db.FrogSSHMysqlHandle import logger
from testcases.FrogLogin import user_name_fb54


def send_msg(user_name_id):
    url = frog["host"] + "/growAlong/v1/api/common/sendSmsV3"
    # print("send_msg_url:{}".format(url))
    header = FrogHeader.get_header()
    print(str(header))
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

def login_fb():
    # user_name_fb = "15800000054"
    send_msg_res = send_msg(13521011463)
    # print("return value:{}".format(send_msg_res))
    assert send_msg_res["code"] == 200
    url = "https://test.frogcool.com/growAlong/v1/api/common/validSmsCode"
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
        "ver": "1.8.50",
        "encrypt": "md5",
        "etag": "qqq",  # 不为空，任意值，与其他接口请求头一致
        "id": id,  # 任意数字
        "sign": str_md5,  # id+key+timestamp加密处理
        "timestamp": timestamp,
        "language": "en",
        "content-type": "application/json"
    }
    print("header:"+str(header))
    # con = MysqlHandle()
    # data = con.select("SELECT sms_code FROM send_sms_mail_rec WHERE user_numbers = {} LIMIT 1".format(user_name_fb54), True)
    # l = data[0]
    data = {
        "areaCode": "86",  # 区号
        "code": "login",
        "smsCode": "1111",  # 验证码
        "type": "mobile",
        "userName": 13521011463  # 登陆手机号
    }
    # frog_req = FrogRequest()
    res = frog_req.post(url, headers=header, json=data)
    logger.info("登陆返回: {}".format(res))
    # print("登陆返回: {}".format(res))
    return res

if __name__ == '__main__':
     # print(send_msg(13521011463))
    print()