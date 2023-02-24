# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：FrogConf.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/11/15 3:46 下午 
'''
import os

pem_path = os.path.dirname(os.path.realpath(__file__))
# print(per_path)


frog = {
    # "host": "https://aws.frogcool.com/",
    "host": "https://test.frogcool.com",
    "key": "846d2cb0c7f09c3ae582c421696d308c",
    "h5key": "csohpmuxayo5rbjmh0ybkriep8vbxks5",
}

UserName = {
    "user_name_fb54": "15800000054",
    "user_name_fb55": "15800000055"

}

ssh_config = {
    "host": "3.141.120.197",  # 跳板机地址
    "port_1": 22,
    "ssh_username": "test-user-ssh",  # 跳转机的用户
    "ssh_pkey": pem_path + os.sep + "test-user-ssh.pem",  # 私钥路径
    "ssh_private_key_password": "voryn",  # 密码（电脑开机密码）
    "remote_bind_address_host": "frog-test-rds-us.c9xsjegjiudt.us-east-2.rds.amazonaws.com",
    "port_2": 3306
}

db_test_config = {
    "host": '127.0.0.1',  # 此处必须是是127.0.0.1
    "user": 'frog_test_query',  # 数据库用户名
    "passwd": 'frog123456789.',  # 数据库密码
    "dbname": 'growalong_prod',  # 数据库名称
}

redis_test_config = {
    "remote_bind_address": 'frog-test-redis-us.qmxst8.clustercfg.use2.cache.amazonaws.com',
    "port_1": 6379,
    "host": '127.0.0.1',
    "port_2": 10022
}

coutry_code = {
    "CN": "86",
    "US": "1",
    "CA": "1",
    "GB": "44",
    "AU": "61"}

p12 = {
    "p12_cert": pem_path + os.sep + "hi.frogcool.com.p12",
    "p12_pw": "kWhgsIiAWFead4NG"
}
print(pem_path + os.sep + "test-user-ssh.pem")