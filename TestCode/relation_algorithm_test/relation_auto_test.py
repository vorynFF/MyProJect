# -*- coding: utf-8 -*-
# author  macklu
import requests
import json
import time


# 这个提供一个联系人，如果这个联系人有2度关系好友，那么输入这个就可以验证2度好友关系是否正确。
def auto_test_2_degree(test_contact):
    file = open("20210615_delete_no_digit.txt", encoding="utf-8")
    lines = file.readlines()
    index = 0  # 首行过滤
    url = "http://t00.me-yun.com:8888/contact/{}/2"  # 补全个人通信录
    base_2_degree_contact = dict()  # 存放有2度人脉，并且已经处理过的contact,用于过滤
    base_no_2degree_contact = dict()  # 没有二度，加入这个里面， 保证遍历的时候没必要重复请求后台
    base_contact_count = dict()  # 这里为了过滤数据量，检测那种通讯录中好友数量大于一定数量，设置：
    process_sep = 15  # 好友数量大于15的才处理
    process_count = 10  # 处理目标二度数据（后面看时间，如果处理快可以考虑所有）
    for line in lines:
        if index == 0:
            index = 1
            continue
        items = line.split("\t")
        if len(items) == 4:
            contact = items[2] + items[1]  # 区号和电话好吗结合
            if contact in base_2_degree_contact.keys() or contact in base_no_2degree_contact.keys():
                continue
            else:
                # time.sleep(0.005)
                try:
                    # 开始请求
                    if contact == test_contact:
                        print(url.format(contact))
                        resp = requests.get(url.format(contact))
                        # jsonData = json.dumps(resp.text)
                        # print(jsonData)
                        if resp.status_code == 200:
                            # 第一步：获取需要判断的目标2度关系数组
                            results = resp.json()
                            if len(results) > 0:
                                base_2_degree_contact[contact] = 1
                                verify_2_degree_result(results, contact)

                except Exception as e:
                    print(str(e))
                    base_no_2degree_contact[contact] = 1


def auto_test_all_2_degree():
    file = open("20210615_delete_no_digit.txt", encoding="utf-8")
    lines = file.readlines()
    index = 0  # 首行过滤
    url = "http://t00.me-yun.com:8888/contact/{}/2"  # 补全个人通信录
    base_2_degree_contact = dict()  # 存放有2度人脉，并且已经处理过的contact,用于过滤
    base_no_2degree_contact = dict()  # 没有二度，加入这个里面， 保证遍历的时候没必要重复请求后台
    base_contact_count = dict()  # 这里为了过滤数据量，检测那种通讯录中好友数量大于一定数量，设置：
    process_sep = 15  # 好友数量大于15的才处理
    process_count = 10  # 处理目标二度数据（后面看时间，如果处理快可以考虑所有）
    for line in lines:
        if index == 0:
            index = 1
            continue
        items = line.split("\t")
        if len(items) == 4:
            contact = items[2] + items[1]  # 区号和电话好吗结合
            if contact not in base_contact_count:
                base_contact_count[contact] = 1
            else:
                base_contact_count[contact] = base_contact_count[contact] + 1
                if base_contact_count[contact] > process_sep:
                    if contact in base_2_degree_contact.keys() or contact in base_no_2degree_contact.keys():
                        continue
                    else:
                        # time.sleep(0.005)
                        try:
                            # 开始请求
                            print(url.format(contact))
                            resp = requests.get(url.format(contact))
                            # jsonData = json.dumps(resp.text)
                            # print(jsonData)
                            if resp.status_code == 200:
                                # 第一步：获取需要判断的目标2度关系数组
                                results = resp.json()
                                if len(results) > 0:
                                    base_2_degree_contact[contact] = 1
                                    verify_2_degree_result(results, contact)
                                else:
                                    base_no_2degree_contact[contact] = 1
                            else:
                                base_no_2degree_contact[contact] = 1
                        except Exception as e:
                            print(str(e))
                            base_no_2degree_contact[contact] = 1


# 判断联系人contact的2度结果是否准确（信息，数量)
def verify_2_degree_result(degree2_results, contact):
    file = open("20210615_delete_no_digit.txt", encoding="utf-8")
    lines = file.readlines()
    # 第二步：获取通讯录数据
    degree_1_array = list()  # 存储 1度 数据
    for line in lines:
        items = line.split("\t")
        if len(items) == 4:
            target_contact = items[2] + items[1]  # 区号和电话好吗结合
            if contact == target_contact:
                if items[3] != "":
                    degree_1_array.append(items[3].strip())

    print("通讯录: ", degree_1_array)

    # 第三部：验证2度关系目标中数据准确性（是否有，权重是否正确）
    print("开始验证:{} 的2度关系是否准确".format(contact))
    for result in degree2_results:
        if len(result) != 2:
            continue
        degree_2_contact = result[0]
        prority = int(result[1])
        # 从1度关系里面找 degree_2_contact.
        is_find = False
        degree_2_contact_count = 0
        for degree_1_contact in degree_1_array:
            for dline in lines:
                ditems = dline.split("\t")
                if len(ditems) != 4:
                    continue
                if ditems[2] + ditems[1] == degree_1_contact and degree_1_contact != contact:  # 从1度好友通讯录找2度好友
                    # print("1-f:",degree_1_contact)
                    if ditems[3].strip() == degree_2_contact:  # 1度好友通讯录里面正好是目标联系人
                        is_find = True
                        degree_2_contact_count = degree_2_contact_count + 1
        print("prority: ", prority, "result_count: ", degree_2_contact_count * 100)
        if is_find and degree_2_contact_count * 100 <= prority:
            print(result, " verify ok !")
        else:
            print(result, "verify failure!")

    # print(degree_1_array)

def test_hello():
    print("hi frog")

if __name__ == "__main__":
    print("hello")
    auto_test_2_degree("8619965225026")
    auto_test_2_degree("8619965225025")

    # auto_test_all_2_degree()
