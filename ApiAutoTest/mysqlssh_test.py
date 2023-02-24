# -*- coding: UTF-8 -*-
'''
@Project ：PyCharm
@File    ：mysqlssh_test.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2021/11/30 
'''
import pymysql
from sshtunnel import SSHTunnelForwarder


with SSHTunnelForwarder(
        ('18.166.156.104', 22),  # 指定ssh登录的跳转机的address，端口号
        ssh_username="test-user-ssh",  # 跳转机的用户
        ssh_pkey="config/test-user-ssh.pem",  # 私钥路径
        ssh_private_key_password="voryn",  # 密码（电脑开机密码）
        remote_bind_address=('frog-test-rds-ap.cwu0cadw1b08.ap-east-1.rds.amazonaws.com', 3306)) as server:  # mysql服务器的address，端口号
    conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                           port=server.local_bind_port,
                           user='frog_test_query',  # 数据库用户名
                           passwd='frog123456789.',  # 数据库密码
                           db='growalong_dev')  # 数据库名称

    cursor = conn.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()；")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    cursor.execute('SELECT * FROM user_info wherelimit 10;')

    # 查询并打印数据
    print(cursor.fetchall())

    cursor.execute("show tables;")
    print(cursor.fetchall())

    # 查询获取info
    cursor.execute("select * from msg_rec_info LIMIT 1;")
    print(cursor.fetchall())