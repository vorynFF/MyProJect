from locust import TaskSet, task, HttpUser, between, events
import queue
import time
import gevent
import os
import random

from FrogHeader import FrogHeader


class LoginTaskSet(TaskSet):


    def on_start(self):
        print("Executing on_start ...")

    def on_stop(self):
        print("Executing on_stop ...")

    @task
    def attentionV2(self):
        """push推送"""
        api = "/frogPush/messagePush/send"
        h = {
            "x-amz-sns-topic-arn": "arn:aws:sns:us-east-2:071094189941:frog_appsFlyerPush_push",
            "x-amz-sns-message-type": "Notification",
            "x-amz-sns-subscription-arn": "arn:aws:sns:us-east-2:071094189941:frog_appsFlyerPush_push:efae4289-b9c2-4624-8d8d-07817e0eac06",
            "x-amz-sns-message-id": "41e9cfe6-2608-56b0-9eb1-954f17f624bb",
            "Content-Type": "text/plain; charset=UTF-8"
        }
        data = r'{"Type":"Notification","MessageId":"feed0db8-fad0-5293-9603-577fad586a1d","TopicArn":"arn:aws:sns:us-east-2:071094189941:user_message_push_send","Message":"{\"msgType\":\"recheckVideo\",     \"busDataMap\":{\"sendUserId\":\"19684853\",\"receiveUserId\":\"69278841\",\"videoId\":\"82855178\"},\"friendUserId\":\"19684853\",\"userId\":\"19684853\"}","Timestamp":"2022-04-06T08:54:32.480Z","SignatureVersion":"1","Signature":"ZBwdfHt9+OprCWr7VyvBmBxNRooM5xaqreJ2Pjr/MptFvAZSJHAnxDbOJjZqoZoe6OtEFZD8vEtF5Q49On/1xQtbSDMbEs0KnUvwM9ehZNu6chyL9bOg+lplihYUhUoTPM+/LgIs7Wf8Mqv2Cm4sGZzqiT8Zt58E2C7uBlfIPrRyzp21/Q/pqMsRRoi9p3doZAkjt5eSnx2PTDPaUaWcJEpypWy/BSquI7cDv8Gs3sGYOvEWmLHHi+WXhcjNFJ4vk5jlHOzDISvvkEsWR+UDTRnFIprqjUO448mi99nCg4UJVSmBtntiQFiuZ17DbQLQYZI6JNhrtu9vhOWzNJi/wg==","SigningCertURL":"https://sns.us-east-2.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:071094189941:user_message_push_send:1b97dbad-9681-44f6-95ef-09da56aeba19"}'
        with self.client.post(api, data=data, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def attentionV2(self):
        """push推送"""
        api = "/frogPush/messagePush/send"
        h = {
            "x-amz-sns-topic-arn": "arn:aws:sns:us-east-2:071094189941:frog_appsFlyerPush_push",
            "x-amz-sns-message-type": "Notification",
            "x-amz-sns-subscription-arn": "arn:aws:sns:us-east-2:071094189941:frog_appsFlyerPush_push:efae4289-b9c2-4624-8d8d-07817e0eac06",
            "x-amz-sns-message-id": "41e9cfe6-2608-56b0-9eb1-954f17f624bb",
            "Content-Type": "text/plain; charset=UTF-8"
        }
        data = r'{"Type":"Notification","MessageId":"feed0db8-fad0-5293-9603-577fad586a1d","TopicArn":"arn:aws:sns:us-east-2:071094189941:user_message_push_send","Message":"{\"msgType\":\"recheckVideo\",     \"busDataMap\":{\"sendUserId\":\"19684853\",\"receiveUserId\":\"69278841\",\"videoId\":\"82855178\"},\"friendUserId\":\"29468478\",\"userId\":\"29468478\"}","Timestamp":"2022-04-06T08:54:32.480Z","SignatureVersion":"1","Signature":"ZBwdfHt9+OprCWr7VyvBmBxNRooM5xaqreJ2Pjr/MptFvAZSJHAnxDbOJjZqoZoe6OtEFZD8vEtF5Q49On/1xQtbSDMbEs0KnUvwM9ehZNu6chyL9bOg+lplihYUhUoTPM+/LgIs7Wf8Mqv2Cm4sGZzqiT8Zt58E2C7uBlfIPrRyzp21/Q/pqMsRRoi9p3doZAkjt5eSnx2PTDPaUaWcJEpypWy/BSquI7cDv8Gs3sGYOvEWmLHHi+WXhcjNFJ4vk5jlHOzDISvvkEsWR+UDTRnFIprqjUO448mi99nCg4UJVSmBtntiQFiuZ17DbQLQYZI6JNhrtu9vhOWzNJi/wg==","SigningCertURL":"https://sns.us-east-2.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:071094189941:user_message_push_send:1b97dbad-9681-44f6-95ef-09da56aeba19"}'
        with self.client.post(api, data=data, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                res.success()
            else:
                res.failure('Failured:{}'.format(res.status_code))

class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]

if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f push.py --web-host="127.0.0.1" --host=https://test.frogcool.com')