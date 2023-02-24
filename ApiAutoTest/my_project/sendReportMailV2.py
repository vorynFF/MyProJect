# -*- coding: UTF-8 -*-
"""
@Project ：PyCharm
@File    ：sendReportMailV2.py
@IDE     ：PyCharm 
@Author  ：fanbo
@Date    ：2022/9/29 
"""

import os
import json
import time
import yagmail
import traceback

def resolveJson():
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep + "allure-report" + os.sep + "widgets" + os.sep + "summary.json"
    with open(path, "rb") as file:
        fileJson = json.load(file)
    field = fileJson['statistic']['failed']
    passed = fileJson['statistic']['passed']
    total = fileJson['statistic']['total']
    broken = fileJson['statistic']['broken']
    time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileJson['time']['start']/1000 + (8*60*60)))
    time_stop = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileJson['time']['stop']/1000 + (8*60*60)))
    time_duration = time.strftime("%M:%S", time.localtime(fileJson['time']['duration']/1000))


    mail_content = f"<b>{time_start} - {time_stop}</b> 运行的接口自动化脚本测试结果如下：<p>运行用例总数：<font color='#0000FF'><b>{total}</b></p>" \
                   f"<p>通过用例数量：<font color='#88C552'><b>{passed}<b></p>" \
                   f"<p>失败用例数量：<font color='#FA4131'><b>{field}<b></p>" \
                   f"<p>中断用例数量：<font color='#FEC840'><b>{broken}<b></p>" \
                   f"<p>运行时长：{time_duration}</p> " \
                   f"<p>详情请见<a href='https://frog-ceshi-data.s3.ap-east-1.amazonaws.com/Allure-Report-Test/index.html'><font color='#0000FF'><b>接口自动化测试报告<b/></a></p>"
    return (mail_content, field, broken)


def getMailAddressList():
    path = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))) + os.sep + "config" + os.sep + "mailAddress.txt"
    mail_address_list = []
    with open(path, 'r') as mail:
        for line in mail:
            line1 = line.strip()
            mail_address_list.append(line1)
    return mail_address_list


'''
receivers 收件人，字符数组['邮件地址']
subject 邮件主题, 字符串
contents 邮件内容，自定义 字符数组
attachments 附件默认为空
'''
def sendEmail(receivers, subject, contents, attachments=[]):
    try:
        # 初始化服务对象直接根据参数给定，更多参考SMTP(）内部
        server = yagmail.SMTP(host='smtp.mxhichina.com', port=465,
                              user='testteam@frogcool.com', password='Frog.188188')
        # 发送内容，设置接受人等信息，更多参考SMTP.send()内部
        server.send(to=receivers,
                    subject=subject,
                    contents=contents,
                    attachments=attachments)
        server.close()
    except Exception:
        print('traceback.format_exc(): {}'.format(traceback.format_exc()))
        return False

    print("邮件发送成功")
    return True
def run():
    '''
    receivers 收件人，字符数组['邮件地址']
    subject 邮件主题, 字符串
    contents 邮件内容，自定义 字符数组
    attachments 附件默认为空
    '''
    receivers = getMailAddressList()
    # receivers = ['fanbo@frogcool.com']
    subject = '接口自动化报告'
    mail_content, field, broken = resolveJson()
    # print(field, passed, total, time_start, time_stop, time_duration)

    # if field > 0 or broken > 0:

    res = sendEmail(receivers, subject, [mail_content])
    # print(mail_content)
    i = 0

    while res is False:
        if i < 2:
            print("重新发送邮件")
            res = sendEmail(receivers, subject, [mail_content])
            i += 1
        else:
            print("邮件发送失败")
            break
    else:
        print("邮件发送成功")
if __name__ == "__main__":
    run()
