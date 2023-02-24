# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：FrogSSHRedis.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/1/24 
"""
import json

from sshtunnel import SSHTunnelForwarder
import redis
from config.FrogConf import ssh_config as ssh
from config.FrogConf import redis_test_config as redis_test
from common.getSystemInfo import get_platform






def redis_server():
    server = SSHTunnelForwarder(
        (ssh['host'], ssh['port_1']),  # 跳板机
        ssh_username=ssh['ssh_username'],
        ssh_pkey=ssh['ssh_pkey'],
        remote_bind_address=(redis_test['remote_bind_address'], redis_test['port_1']),  # 远程的Redis服务器
        local_bind_address=('0.0.0.0', redis_test['port_2'])
    )
    return server


#  获取字符串类型的值
def str_get(key):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.get(key)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.get(key)
        server.close()
    return res


# 插入k，v值
def str_set(key, value, time=None):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        r.set(key, value, time)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        r.set(key, value, time)
        server.close()


# 删除
def str_delete(key):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        tag = r.exists(key)
        if tag:
            r.delete(key)
            print("key: {} 删除成功".format(key))
        else:
            print("无此key")

    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        tag = r.exists(key)
        if tag:
            r.delete(key)
            print("key: {} 删除成功".format(key))
        else:
            print("无此key")
        server.close()



# 获取key的值是hash类型的数据
def hash_get(name, key):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.hget(name, key)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.hget(name, key)
        server.close()
    return res


# hash类型是set，设置值
def hash_set(name, key, value):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        r.hset(name, key, value)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        r.hset(name, key, value)
        server.close()


# hash 类型获取key里面所有类型
def hash_getall(name):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.hgetall(name)
        data = {}
        if res:
            for k, v in res.items():
                data[k] = v
            return data
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.hgetall(name)
        server.close()
        data = {}
        if res:
            for k, v in res.items():
                data[k] = v
            return data
    return None


# hash删除某个key
def hash_del(name, key):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        tag = r.hdel(name, key)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        tag = r.hdel(name, key)
        server.close()
    if tag:
        print("name:{}, key: {} 删除成功".format(name, key))
        return 0
    else:
        print("删除失败")
        return 1
def zset_getmax(name, count=None):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.zpopmax(name, count)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.zpopmax(name, count)
        server.close()
    return res
def zset_getcount(name):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.zcard(name)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.zcard(name)
        server.close()
    return res
def zset_getall(name, desc=True, withscores=True):
    if get_platform():
        r = redis.Redis(host=redis_test['remote_bind_address'], port=redis_test['port_1'], db=0,
                        decode_responses=True)
        res = r.zrange(name, 0, -1, desc, withscores)
    else:
        server = redis_server()
        server.start()
        r = redis.Redis(host=redis_test['host'], port=server.local_bind_port, db=0,
                        decode_responses=True)
        res = r.zrange(name, 0, -1, desc, withscores)
        server.close()

    return res


if __name__ == "__main__":

    # key = "videoPond:data:pond:user:videoGroupTypeScore:33769113"
    # item = hash_getall(key)
    # print(item)
    # key4 = "videoPond:data:pond:video:group:userGetVideoList:33769113"
    # print(hash_getall(key4))
    key2 = "videoPond:data:pond:video:group:userGetUserList:33769113"
    print(zset_getall(key2))
    # for key, value in item:
    #     print(value)
    # key3 = "videoPond:data:pond:video:group:userListVideoScore:lessTwelve:33769113"
    # print(zset_getall(key3))

    # for i in zset_getall("user:videoTag:1:getTagSubListRanking"):
    #     print(i)
    #     print(type(i))
    #     y = i[0]
    #     eval(y)
    #     print(type(eval(y)))
    # print(type(zz))


    # server = redis_server()
    # server.start()
    # r = redis.Redis(host=redis_test['host'], port=server.local_bind_port,
    #                 db=0, decode_responses=True)  # 如果设置了密码，就加上password=密码
    # print(r.keys("*"))
    ""
    # print(str_delete("user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:58804776"))
    # print(hash_get("videoPond:data:vlog:video:friend:list:12262332", "82538177"))
    # print(hash_get("user:api:FriendOLK:list", 1000000000))

    # print(hash_del(name, user_id))
    # print(hash_del("user:api:FriendOLK:list:", 1000000000))
    # # print(hash_set("user:api:FriendOLK:list:", 1000000000, "12"))
    # print(hash_get("user:api:FriendOLK:list:", 1000000000))
    # print(hash_getall("user:pool:data:userRanking:userVideo:getListGain:userId:228405"))
    # print(r.hget("user:pool:data:userRanking:userVideo:getListGain:userId:228405", "164410"))
    # val = str_get("limit_7F531930-0D08-4734-A017-475803803660_registerAndLogin_DID_8")
    # print(str_delete("user:pool:data:userRanking:userVideo:saveVideoBirthday:userId:58804776"))
    # print(type(val))
    # val_dict = json.loads(val)
    # print(val_dict["headImgUrl"])
    # server.close()
