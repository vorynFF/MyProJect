# -*- coding: UTF-8 -*-
"""
@Project ：FrogApiAutoTest
@File    ：Loggers.py
@IDE     ：PyCharm
@Author  ：luxiaosan
@Date    ：2021/11/19 10:04 上午
"""
import os
import sys
import logging
import time
from utils.JarProjectUtil import JarProjectUtil
import re

class ColoredFormatter(logging.Formatter):
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')

    def __init__(self, fmt=None, datefmt=None, style='%', use_color=True):
        super().__init__(fmt, datefmt, style)
        self.use_color = use_color

    def format(self, record):
        msg = super().format(record)
        if self.use_color and record.levelname in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            if record.levelname == 'DEBUG':
                msg = f'\033[1;34m{msg}\033[0m'
            elif record.levelname == 'INFO':
                msg = f'\033[1;32m{msg}\033[0m'
            elif record.levelname == 'WARNING':
                msg = f'\033[1;33m{msg}\033[0m'
            elif record.levelname == 'ERROR':
                msg = f'\033[1;31m{msg}\033[0m'
            elif record.levelname == 'CRITICAL':
                msg = f'\033[1;41m{msg}\033[0m'
        return msg

class StripAnsiHandler(logging.StreamHandler):
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')

    def emit(self, record):
        try:
            msg = self.ansi_escape.sub('', record.msg)
            record.msg = msg
            super().emit(record)
        except Exception:
            self.handleError(record)



class Loggers(object):
    """
    日志处理类
    """

    def __init__(self, level=logging.DEBUG):
        """
        :param path: 日志路径
        :param level: 日志打印级别
        """
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d_")
        self.log_path = JarProjectUtil.project_root_path() + "/log/"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        self.log_name = self.log_path + self.log_time + 'test.log'
        # 创建一个日志器logger并设置其日志级别为DEBUG
        self.logger = logging.getLogger(self.log_name)
        # self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)


        self.logger.handlers.clear()

        if not self.logger.handlers:

            # 创建一个日志器logger并设置其日志级别为DEBUG
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)



            formatter = ColoredFormatter('%(asctime)s [%(filename)s:[line:%(lineno)d]] [%(levelname)s] - %(message)s', use_color=True)

            handler.setFormatter(formatter)


            self.logger.addHandler(handler)


            # 设置文件日志
            file_handler = logging.FileHandler(self.log_name, encoding="utf-8")
            formatter = logging.Formatter('%(asctime)s [%(filename)s:[line:%(lineno)d]] [%(levelname)s] - %(message)s')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)



    def debug(self, message, *args, **kwargs):
        """
        :param message: debug信息
        :return:
        """
        kwargs['stacklevel'] = 2
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """
        :param message: info信息
        :return:
        """
        kwargs['stacklevel'] = 2
        self.logger.info(message, *args, **kwargs)

    def warn(self, message, *args, **kwargs):
        """
        :param warn: warn 信息
        :return:
        """
        kwargs['stacklevel'] = 2
        self.logger.warning(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """
        :param message: critical 信息
        :return:
        """
        kwargs['stacklevel'] = 2
        self.logger.critical(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """
        :param message: error 信息
        :return:
        """
        kwargs['stacklevel'] = 2
        self.logger.error(message, *args, **kwargs)



if __name__ == "__main__":
    mylogger = Loggers()
    mylogger.debug('debug……')
    mylogger.info('info……')
    mylogger.warn('warn……')
    mylogger.critical('critical……')
    mylogger.error('error……')
