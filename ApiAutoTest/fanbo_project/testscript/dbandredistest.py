# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：dbandredistest.py
@IDE     ：PyCharm
@Author  ：fanbo
@Date    ：2022/2/23
"""
from db.FrogSSHMysqlHandle import MysqlHandle
import FrogSSHRedis

user_name = "Yeezy52@qq.com"


conn = MysqlHandle()
select_sql = "select * from user_info where user_name = \"%s\";"% user_name
print("查询语句：" + select_sql)
data = conn.select(select_sql, True)
print(f"查询结果：{data}")
user_id = data[0]
print(f"userid：{user_id}")
del_sql = "delete from user_phone_address_book where user_id = %d;"% user_id
print("删除语句：" + del_sql)
delete = conn.delete(del_sql)
print(f"删除结果：{delete}")
up_sql = "update index_msg_info_add_friend set del_flag = 1 where friend_user_id = %d;"% user_id
print("更新语句：" + up_sql)
updata = conn.updata(up_sql)
print(f"更新语句：{updata}")

name = "user:userFriendsPhoneBookQuickAddModelList:userId:{}".format(user_id)
name2 = "user:userFriendsQuickAddModelList:userId:{}".format(user_id)
print(name)
print(name2)
phone = FrogSSHRedis.hash_getall(name)
phone2 = FrogSSHRedis.hash_getall(name2)

print(phone)
print(phone2)
if phone is not None:
    for key, value in phone.items():
        print(key)
        print(FrogSSHRedis.hash_del(name, key))
if phone2 is not None:
    for key2, value2 in phone2.items():
        print(key2)
        print(FrogSSHRedis.hash_del(name2, key2))
