# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：sendReportMail.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/3/31 
"""
import os
import json
import time
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header



def resolveJson():
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep + "allure-report" + os.sep + "widgets" + os.sep + "summary.json"

    file = open(path, "rb")
    fileJson = json.load(file)
    field = fileJson['statistic']['failed']
    passed = fileJson['statistic']['passed']
    total = fileJson['statistic']['total']
    broken = fileJson['statistic']['broken']
    time_start = fileJson['time']['start']
    time_stop = fileJson['time']['stop']
    time_duration = fileJson['time']['duration']



    return (field, passed, broken, total, time_start, time_stop, time_duration)



def sendMail(mail_content):


    path = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + os.sep + "config" + os.sep + "mailAddress.txt"

    host_server = 'smtp.mxhichina.com'  # 阿里云企业邮箱smtp服务器
    sender = 'testteam@frogcool.com'  # 发件人邮箱
    pwd = 'Frog.188188'

    mail_address_list = []
    with open(path, 'r') as mail:
        for line in mail:
            line1 = line.strip()
            mail_address_list.append(line1)

    receiver = mail_address_list
    mail_title = '接口自动化报警邮件'  # 邮件标题

    # 邮件正文内容

    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender
    msg["To"] = Header(",".join(mail_address_list), "utf-8")

    msg.attach(MIMEText(mail_content, 'html'))

    try:
        smtp = SMTP_SSL(host_server)  # ssl登录连接到邮件服务器
        smtp.set_debuglevel(1)  # 0是关闭，1是开启debug
        smtp.ehlo(host_server)  # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
        smtp.login(sender, pwd)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")


if __name__ == '__main__':
    result = resolveJson()
    field = result[0]
    passed = result[1]
    broken = result[2]
    total = result[3]
    time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[4]/1000 + (8*60*60)))
    time_stop = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[5]/1000 + (8*60*60)))
    time_duration = time.strftime("%M:%S", time.localtime(result[6]/1000))
    # print(field, passed, total, time_start, time_stop, time_duration)
    if field > 0 or broken > 0:
        mail_content = "%s - %s 运行的接口自动化脚本测试结果如下：<p>运行用例总数：%d</p><p>通过用例数量：%d</p><p>失败用例数量：%d</p><p>中断用例数量：%d</p><p>运行时长：%s</p> <p>详情请见<a href='https://frog-ceshi-data.s3.ap-east-1.amazonaws.com/Allure-Report-Test/index.html'>接口自动化测试报告</a></p>" % (time_start, time_stop, total, passed, field, broken, time_duration)
        res = sendMail(mail_content)
        print(res)
    # print(type(result[4]))
    # pwd = 'pwd't
    # d = os.system(pwd)
    # print(d)