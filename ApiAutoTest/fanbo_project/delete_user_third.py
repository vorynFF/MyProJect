# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：delete_user_third.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/10/13 
"""
import FrogSSHRedis
from db.FrogSSHMysqlHandle import MysqlHandle

con = MysqlHandle()
def delete_user_third(fid):

    aa = "select * from growalong_dev.user_info where frog_id = {};".format(fid)
    data2 = con.select(sql=aa, one=True)
    userId = data2[0]
    key = ["login:api:user:{}".format(userId), "api:user:{}:sessionUser".format(userId)]
    for i in key:
        rdata = FrogSSHRedis.str_delete(i)
        print(rdata)

    sql = ["delete from growalong_dev.user_third_party_apple where user_id = {};".format(userId),
           "delete from growalong_dev.user_info where id = {};".format(userId),
           "delete from growalong_dev.user_third_party_google where user_id = {};".format(userId)]
    for a in sql:
        data = con.delete(sql=a)
        print(data)

if __name__ == '__main__':

    fid = "7401996861"  # 新注册的frog_id

    delete_user_third(fid)