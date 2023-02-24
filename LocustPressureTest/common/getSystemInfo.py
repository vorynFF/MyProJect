# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：getSystemInfo.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/2/16 
"""
import platform


def get_platform():
    getPlatform = platform.platform()
    print(getPlatform)
    if "Linux" in getPlatform:
        print("=====================在服务器运行=====================在服务器运行=====================在服务器运行=====================")
        return True
    elif "Windows" in getPlatform:
        print("=====================在windows服务器运行=====================在windows服务器运行=====================在windows服务器运行=====================")
        return False
    else:
        print("=====================在本地运行=====================在本地运行=====================在本地运行=====================")
        return False