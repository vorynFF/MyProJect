
"""
explore:video:lock:用户id:朋友id   -- 用户频率限制的key

explore:video:data:用户id:朋友id  -- 存放用户数据的key

explore:chat:send_wyd_counts:key:加密的key    -- 用户wyd频率限制的key

explore:chat:max_uninterrupted_days:key:加密的key    -- 用户最大连续聊天频率限制的key

select * from chat_max_uninterrupted_days; -- 用户最大连续聊天数据表

select * from chat_send_wyd_counts; -- 用户wyd次数数据表
"""

import FrogSSHRedis as redisA
from db.FrogSSHMysqlHandle import MysqlHandle

con = MysqlHandle()
def delete_wyd_lock(uid, fuid):
    sql = "select encryption_key from frog_chat_im.twilio_conversation where left_user_id = {} and right_user_id = {}".format(uid, fuid)
    data = con.select(sql=sql, one=True)
    print(data)
    key = "explore:chat:send_wyd_counts:key:" + data[0]
    print(redisA.str_delete(key))

def delete_video_lock(uid, fuid):
    key = "explore:video:lock:" + uid + ":" + fuid
    print(redisA.str_delete(key))
def delete_im_lock(uid, fuid):
    sql = "select encryption_key from frog_chat_im.twilio_conversation where left_user_id = {} and right_user_id = {}".format(uid, fuid)
    data = con.select(sql=sql, one=True)
    print(data)

    key = "explore:chat:max_uninterrupted_days:key:" + data[0]
    print(redisA.str_delete(key))

if __name__ == '__main__':
    uid = "33769113"
    fuid = "38229741"
    # delete_video_lock(uid, fuid)  # 用户频率限制的key
    delete_wyd_lock(uid, fuid)  # 用户wyd频率限制的key
    # delete_im_lock(uid, fuid)  # 用户最大连续聊天频率限制的key