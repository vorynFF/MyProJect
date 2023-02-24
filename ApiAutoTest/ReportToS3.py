# -*- coding: UTF-8 -*-
'''
@Project ：FrogApiAutoTest 
@File    ：FrogReportToS3.py
@IDE     ：PyCharm 
@Author  ：luxiaosan
@Date    ：2022/1/22 6:17 下午 
'''
import os


def upload_test_report():
    target_dir = 'allure-report'
    # 获取当前路径
    abs_path = os.path.dirname(os.path.realpath(__file__))
    print(abs_path)
    report_path = abs_path + os.sep + target_dir + os.sep
    if os.path.exists:
        # 删除s3目标文件夹内容
        os.system('aws s3 rm s3://frog-ceshi-data/Allure-Report-Test/ --recursive')
        # 拷贝新的
        os.system('aws s3 cp {}  s3://frog-ceshi-data/Allure-Report-Test/ --recursive'.format(report_path))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    upload_test_report()
