# -*- coding: UTF-8 -*-
'''
@Project ：Locust 
@File    ：frog_fixture_press.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2022/2/22 9:21 上午 
'''
from locust import TaskSet, task, HttpUser, between, events
import queue
import time
import gevent
import os
import random
from add_buddy import LoginTaskSet as budd_set
from query_information import LoginTaskSet as information_set
from query_user_and_video_information import LoginTaskSet as user_video_info_set
from video_playback_query import LoginTaskSet as video_query_set
from save_user_information import LoginTaskSet as save_user_info_set
from Save_the_video import LoginTaskSet as save_video_set
from save_the_information import LoginTaskSet as save_info_set
from less_traffic_dpi import LoginTaskSet as less_set


class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    # 启动人数一定要是tasks的长度的整数倍
    tasks = [budd_set, information_set, user_video_info_set,
             video_query_set, save_user_info_set,
             save_info_set, less_set]
    """准备测试数据"""
    queue_data = queue.Queue()
    tel_to_frienduserid = []
    file = open(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)) + os.sep + "user_info.sql", "r")
    content = file.readlines()
    for line in content:
        items = line.split("|")
        if len(items) == 4:
            key = items[2].strip()
            value = items[0].strip()
            tel_to_frienduserid.append(value)
            area = items[1].strip()
            userinfo = area + "|" + key
            queue_data.put_nowait(userinfo)


if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f frog_fixture_press.py --web-host="127.0.0.1" --host=https://test.frogcool.com')
