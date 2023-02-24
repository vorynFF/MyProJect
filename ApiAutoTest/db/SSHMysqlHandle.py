# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：FrogMysqlHandle.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2021/12/3 4:35 下午 
'''
import pymysql
from sshtunnel import SSHTunnelForwarder
from utils.Loggers import Loggers
from config.FrogConf import ssh_config as ssh
from config.FrogConf import db_test_config as db
from common.getSystemInfo import get_platform

logger = Loggers()


class MysqlHandle(object):

    def __init__(self):
        print("sshdb init")

    def select(self, sql, one=False):
        if get_platform():
            self.conn = pymysql.connect(host=ssh['remote_bind_address_host'],  # 此处必须是是127.0.0.1
                                        port=ssh['port_2'],
                                        user=db['user'],  # 数据库用户名
                                        passwd=db['passwd'],  # 数据库密码
                                        db=db['dbname'])  # 数据库名称
            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sql)
                if one:
                    return self.cursor.fetchone()
                else:
                    return self.cursor.fetchall()
            except Exception as e:
                logger.error("查询数据库异常: {}, 异常信息: {}".format(sql, str(e)))
            finally:
                self.cursor.close()
                self.conn.close()
        else:
            with SSHTunnelForwarder(
                    (ssh['host'], ssh['port_1']),  # 指定ssh登录的跳转机的address，端口号
                    ssh_username=ssh['ssh_username'],  # 跳转机的用户
                    ssh_pkey=ssh['ssh_pkey'],  # 私钥路径
                    # ssh_private_key_password=ssh["ssh_private_key_password"],  # 密码（电脑开机密码）
                    remote_bind_address=(
                            ssh['remote_bind_address_host'],
                            ssh['port_2'])) as server:  # mysql服务器的address，端口号
                self.conn = pymysql.connect(host=db['host'],  # 此处必须是是127.0.0.1
                                            port=server.local_bind_port,
                                            user=db['user'],  # 数据库用户名
                                            passwd=db['passwd'],  # 数据库密码
                                            db=db['dbname'])  # 数据库名称

                try:
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(sql)
                    if one:
                        return self.cursor.fetchone()
                    else:
                        return self.cursor.fetchall()
                except Exception as e:
                    logger.error("查询数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                finally:
                    self.cursor.close()
                    self.conn.close()

    def insert(self, sql):
        if get_platform():
            self.conn = pymysql.connect(host=ssh['remote_bind_address_host'],  # 此处必须是是127.0.0.1
                                        port=ssh['port_2'],
                                        user=db['user'],  # 数据库用户名
                                        passwd=db['passwd'],  # 数据库密码
                                        db=db['dbname'])  # 数据库名称

            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error("查询数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                self.conn.rollback()
            finally:
                self.cursor.close()
                self.conn.close()
        else:
            with SSHTunnelForwarder(
                    (ssh['host'], ssh['port_1']),  # 指定ssh登录的跳转机的address，端口号
                    ssh_username=ssh['ssh_username'],  # 跳转机的用户
                    ssh_pkey=ssh['ssh_pkey'],  # 私钥路径
                    # ssh_private_key_password=ssh["ssh_private_key_password"],  # 密码（电脑开机密码）
                    remote_bind_address=(
                            ssh['remote_bind_address_host'],
                            ssh['port_2'])) as server:  # mysql服务器的address，端口号
                self.conn = pymysql.connect(host=db['host'],  # 此处必须是是127.0.0.1
                                            port=server.local_bind_port,
                                            user=db['user'],  # 数据库用户名
                                            passwd=db['passwd'],  # 数据库密码
                                            db=db['dbname'])  # 数据库名称

                try:
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    logger.error("查询数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                    self.conn.rollback()
                finally:
                    self.cursor.close()
                    self.conn.close()

    def delete(self, sql):
        if get_platform():
            self.conn = pymysql.connect(host=ssh['remote_bind_address_host'],  # 此处必须是是127.0.0.1
                                        port=ssh['port_2'],
                                        user=db['user'],  # 数据库用户名
                                        passwd=db['passwd'],  # 数据库密码
                                        db=db['dbname'])  # 数据库名称
            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error("删除数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                self.conn.rollback()
            finally:
                self.cursor.close()
                self.conn.close()
        else:
            with SSHTunnelForwarder(
                    (ssh['host'], ssh['port_1']),  # 指定ssh登录的跳转机的address，端口号
                    ssh_username=ssh['ssh_username'],  # 跳转机的用户
                    ssh_pkey=ssh['ssh_pkey'],  # 私钥路径
                    ssh_private_key_password=ssh["ssh_private_key_password"],  # 密码（电脑开机密码）
                    remote_bind_address=(
                            ssh['remote_bind_address_host'],
                            ssh['port_2'])) as server:  # mysql服务器的address，端口号
                self.conn = pymysql.connect(host=db['host'],  # 此处必须是是127.0.0.1
                                            port=server.local_bind_port,
                                            user=db['user'],  # 数据库用户名
                                            passwd=db['passwd'],  # 数据库密码
                                            db=db['dbname'])  # 数据库名称

                try:
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    logger.error("删除数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                    self.conn.rollback()
                finally:
                    self.cursor.close()
                    self.conn.close()

    def updata(self, sql):
        if get_platform():
            self.conn = pymysql.connect(host=ssh['remote_bind_address_host'],  # 此处必须是是127.0.0.1
                                        port=ssh['port_2'],
                                        user=db['user'],  # 数据库用户名
                                        passwd=db['passwd'],  # 数据库密码
                                        db=db['dbname'])  # 数据库名称
            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error("删除数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                self.conn.rollback()
            finally:
                self.cursor.close()
                self.conn.close()
        else:
            with SSHTunnelForwarder(
                    (ssh['host'], ssh['port_1']),  # 指定ssh登录的跳转机的address，端口号
                    ssh_username=ssh['ssh_username'],  # 跳转机的用户
                    ssh_pkey=ssh['ssh_pkey'],  # 私钥路径
                    ssh_private_key_password=ssh["ssh_private_key_password"],  # 密码（电脑开机密码）
                    remote_bind_address=(
                            ssh['remote_bind_address_host'],
                            ssh['port_2'])) as server:  # mysql服务器的address，端口号
                self.conn = pymysql.connect(host=db['host'],  # 此处必须是是127.0.0.1
                                            port=server.local_bind_port,
                                            user=db['user'],  # 数据库用户名
                                            passwd=db['passwd'],  # 数据库密码
                                            db=db['dbname'])  # 数据库名称

                try:
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    logger.error("更新数据库异常: {}, 异常信息: {}".format(sql, str(e)))
                    self.conn.rollback()
                finally:
                    self.cursor.close()
                    self.conn.close()
con = MysqlHandle()
sql = "SELECT * FROM user_info WHERE user_name = 'danyitest@qq.com';"
data = con.select(sql=sql, one=True)
print(data)
# # friend_user_id = data[0]
# for i in data:方法
#     print("1212", i)
#     for y in i:
#         print("232322", y)