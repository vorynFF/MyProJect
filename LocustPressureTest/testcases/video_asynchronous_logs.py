from locust import TaskSet, task, HttpUser, between, events
import requests
import os


class LoginTaskSet(TaskSet):


    def on_start(self):
        print("Executing on_start ...")

    def on_stop(self):
        print("Executing on_stop ...")

    @task
    def s3uploadstart(self):
        """视频上传开始"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/s3upload/start'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{  "Type" : "Notification",  "MessageId" : "395d6da5-02b8-564d-bdc5-370790a3a27a", "TopicArn" : "arn:aws:sns:us-east-1:071094189941:S3AddVideoSnsFrog", "Subject" : "Amazon S3 Notification", "Message" : {"Records": [{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2022-03-09T11:30:33.917Z", "eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROARBDMLH524TMTLEMYH:CognitoIdentityCredentials"}, "requestParameters":{"sourceIPAddress":"104.149.179.122"}, "responseElements":{"x-amz-request-id":"YN22DNJECT3PCCW7", "x-amz-id-2":"lW8XlCGlwaPaS7vDTCHufFzTa7p/aa0NDVftcVpNQ0+8iFrx9+3Orf5CCweCFeb+CCYYdCQWM9EXaC2xh9FzAbCiPUHa24oI"}, "s3":{"s3SchemaVersion":"1.0","configurationId":"S3AddVideoSnsFrog", "bucket":{"name":"amplify-frogandroiden-dev-181449-deployment181449-dev","ownerIdentity": {"principalId":"A3QMBZLM0ET1NO"},"arn":"arn:aws:s3:::amplify-frogandroiden-dev-181449-deployment181449-dev"}, "object":{"key":"public/frog/android/video/2239193039150.mp4","size":1167294,"eTag":"f5da34ad28f26985c385d6caa951ab8b", "versionId":"..SMAcFra26tJGxjuJKB4LS4AXjrl.L0","sequencer":"0062288FD9BAC482DD"}}}]}, "Timestamp" : "2022-03-09T11:30:35.052Z",  "SignatureVersion" : "1", "Signature" : "FwVh/Ec7mNCoCfANv2yjOK5LQ3j2lFDW5bbigVdPoTc/OF598NCbNaM69IAh23+9NGT2nGymx0ILG+606i96JZbFG0RRb7TsZgFLEIgTKfuNaEFk5jO4MFUPHohqxwkBAXmiLABUPm/sNmE/cjjOAE0ZQ0plY1pY73QSW0uDU8Stp3uFsHehM80/mOilUIIgtQZG4vF4BtLXyNSCXNiiWEwrR0HfSCZdVTVO5NvyfDNTS2TLm9iBiaRfBJ9jxg2IcJ4e0xbHIYjR1wnMQXQS6ovhna4G8DdpN13q7nO9QkM07fr9LKawIYqJm3z4FbtZsOrWXenRaO60pj8ZmIO1mg==", "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",  "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:S3AddVideoSnsFrog:0f7fe8bb-befc-43a9-81c5-ea51c13aa09f"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def s3uploadend(self):
        """视频上传结束"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/s3upload/end'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{  "Type" : "Notification",  "MessageId" : "395d6da5-02b8-564d-bdc5-370790a3a27a", "TopicArn" : "arn:aws:sns:us-east-1:071094189941:S3AddVideoSnsFrog", "Subject" : "Amazon S3 Notification", "Message" : {"Records": [{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2022-03-09T11:30:33.917Z", "eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROARBDMLH524TMTLEMYH:CognitoIdentityCredentials"}, "requestParameters":{"sourceIPAddress":"104.149.179.122"}, "responseElements":{"x-amz-request-id":"YN22DNJECT3PCCW7", "x-amz-id-2":"lW8XlCGlwaPaS7vDTCHufFzTa7p/aa0NDVftcVpNQ0+8iFrx9+3Orf5CCweCFeb+CCYYdCQWM9EXaC2xh9FzAbCiPUHa24oI"}, "s3":{"s3SchemaVersion":"1.0","configurationId":"S3AddVideoSnsFrog", "bucket":{"name":"amplify-frogandroiden-dev-181449-deployment181449-dev","ownerIdentity": {"principalId":"A3QMBZLM0ET1NO"},"arn":"arn:aws:s3:::amplify-frogandroiden-dev-181449-deployment181449-dev"}, "object":{"key":"public/frog/android/video/2239193039150.mp4","size":1167294,"eTag":"f5da34ad28f26985c385d6caa951ab8b", "versionId":"..SMAcFra26tJGxjuJKB4LS4AXjrl.L0","sequencer":"0062288FD9BAC482DD"}}}]}, "Timestamp" : "2022-03-09T11:30:35.052Z",  "SignatureVersion" : "1", "Signature" : "FwVh/Ec7mNCoCfANv2yjOK5LQ3j2lFDW5bbigVdPoTc/OF598NCbNaM69IAh23+9NGT2nGymx0ILG+606i96JZbFG0RRb7TsZgFLEIgTKfuNaEFk5jO4MFUPHohqxwkBAXmiLABUPm/sNmE/cjjOAE0ZQ0plY1pY73QSW0uDU8Stp3uFsHehM80/mOilUIIgtQZG4vF4BtLXyNSCXNiiWEwrR0HfSCZdVTVO5NvyfDNTS2TLm9iBiaRfBJ9jxg2IcJ4e0xbHIYjR1wnMQXQS6ovhna4G8DdpN13q7nO9QkM07fr9LKawIYqJm3z4FbtZsOrWXenRaO60pj8ZmIO1mg==", "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",  "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:S3AddVideoSnsFrog:0f7fe8bb-befc-43a9-81c5-ea51c13aa09f"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videocoverstart(self):
        """封面截图开始"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videocover/start'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"dacd5261-b55f-538a-8d21-08c33c92052d","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_CoverScreenshot_start","Message":{"dataSign":"37a6259cc0c1dae299a7866489dff0bd","dateTime":1646823308957,"type":"VIDEO_COVER","videoId":"78837586","videoUrl":"https://dx265v3f1t09x.cloudfront.net/public/frog/android/video/2239185457880.mp4"},"Timestamp":"2022-03-09T10:55:09.123Z","SignatureVersion":"1","Signature":"CdYtLGUSi4y+BHPVIy7t8NbTCWg0dL161ohD8Y3l4JTvdjjdwSIDstQ6CRYnavUpFhvI11J0Il3/GL9ofSona8vjif+Ia68/Zif6pBmya9KiSArPe4DxhyQbCVisuz0aNMj+te2idVlIaFiUq1GAflgRxWalTqLb5vQqrggqOIL6h/KQ6V5yWJ7Fy5XFDHLHDzS/XvP7GxxDjw7zTk1aBkimmyMefmkp+aYuTjTyU8oGRk7iRSJIhcj9vqqvujKnok+F7Tb9SuiDUdDFrwSmh5MjQ0GsN/B0sp+zl7pclXLKwOL10fHandmxf/O3dHSVXVj6dpAPvIfs+gIihZbAFw==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_CoverScreenshot_start:4dc00cd1-cba5-4f36-9dd3-88d946e5e524"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videocoverend(self):
        """封面截图结束"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videocover/end'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"dacd5261-b55f-538a-8d21-08c33c92052d","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_CoverScreenshot_start","Message":{"dataSign":"37a6259cc0c1dae299a7866489dff0bd","dateTime":1646823308957,"type":"VIDEO_COVER","videoId":"78837586","videoUrl":"https://dx265v3f1t09x.cloudfront.net/public/frog/android/video/2239185457880.mp4"},"Timestamp":"2022-03-09T10:55:09.123Z","SignatureVersion":"1","Signature":"CdYtLGUSi4y+BHPVIy7t8NbTCWg0dL161ohD8Y3l4JTvdjjdwSIDstQ6CRYnavUpFhvI11J0Il3/GL9ofSona8vjif+Ia68/Zif6pBmya9KiSArPe4DxhyQbCVisuz0aNMj+te2idVlIaFiUq1GAflgRxWalTqLb5vQqrggqOIL6h/KQ6V5yWJ7Fy5XFDHLHDzS/XvP7GxxDjw7zTk1aBkimmyMefmkp+aYuTjTyU8oGRk7iRSJIhcj9vqqvujKnok+F7Tb9SuiDUdDFrwSmh5MjQ0GsN/B0sp+zl7pclXLKwOL10fHandmxf/O3dHSVXVj6dpAPvIfs+gIihZbAFw==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_CoverScreenshot_start:4dc00cd1-cba5-4f36-9dd3-88d946e5e524"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videotrancodestart(self):
        """封面转码开始"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videotrancode/start'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"391c4a1d-2c8a-5550-a714-10bf5a1a4375","TopicArn":"arn:aws:sns:us-east-1:071094189941:frogo1-SnsTopic-5VHIY5478B4U","Subject":"Workflow Status:: Complete:: e7faceb6-1d7f-4c15-8a21-368e08ef1687","Message":{"encodeJobId":"1646818369126-ebmfok","frameCapture":false,"acceleratedTranscoding":"DISABLED","workflowTrigger":"Video","cloudFront":"d4egpzynfumwb.cloudfront.net","archiveSource":"DISABLED","enableSqs":true,"srcBucket":"frogo1-source-1ftxknfo61kxc","inputRotate":"DEGREE_0","srcWidth":624,"destBucket":"frogo1-destination-otp4l535tez","workflowStatus":"Complete","workflowName":"frogo1","encodingProfile":720,"isCustomTemplate":false,"startTime":"2022-03-09T09:32:45.802Z","enableMediaPackage":false,"jobTemplate":"frogo1_Ott_720p_Avc_Aac_16x9_qvbr","enableSns":true,"srcVideo":"public/frog/android/video/223920131265.mp4","srcHeight":1280,"endTime":"2022-03-09T09:33:03.125Z","hlsPlaylist":"s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/hls/223920131265.m3u8","hlsUrl":"https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/hls/223920131265.m3u8","mp4Outputs":["s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.mp4","s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.0000001.jpg"],"mp4Urls":["https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.mp4","https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.0000001.jpg"],"guid":"e7faceb6-1d7f-4c15-8a21-368e08ef1687"},"Timestamp":"2022-03-09T09:33:04.041Z","SignatureVersion":"1","Signature":"DMSxW8w3C+rhPrfpNwb0UBhd5IP2nxxKjfc0zUzD897/iR1GwqwTDx75nDUV1KMbqiKI14m70r1ureDp2lsIl/kakQda+fMXMXRAvIh/308czTnHAVsGWN5e0T2xFn7crgLdAEgGIcTlFqYgWb2JeC36OsM93rc2EU2h5ALOtN6D/XLagszFZWn0ljNAC0jtD3dbapyNkL4hqssUKSsfCVRTNFJaqDabcrH2yM3Iv/YAbhXuk8GbyETuGvSxswfu0bx/v0fMLvaDQsXVs2QJm/6XoAtUyXvim1zoO1Za3mdHIFcQbYvkhSY771kroSaWdpuBeZ3nFXwGDt+m8Ry+6g==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:frogo1-SnsTopic-5VHIY5478B4U:4dc1cf81-0065-4f88-a185-be3b037e5937"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videotrancodeend(self):
        """封面转码结束"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videocover/end'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"391c4a1d-2c8a-5550-a714-10bf5a1a4375","TopicArn":"arn:aws:sns:us-east-1:071094189941:frogo1-SnsTopic-5VHIY5478B4U","Subject":"Workflow Status:: Complete:: e7faceb6-1d7f-4c15-8a21-368e08ef1687","Message":{"encodeJobId":"1646818369126-ebmfok","frameCapture":false,"acceleratedTranscoding":"DISABLED","workflowTrigger":"Video","cloudFront":"d4egpzynfumwb.cloudfront.net","archiveSource":"DISABLED","enableSqs":true,"srcBucket":"frogo1-source-1ftxknfo61kxc","inputRotate":"DEGREE_0","srcWidth":624,"destBucket":"frogo1-destination-otp4l535tez","workflowStatus":"Complete","workflowName":"frogo1","encodingProfile":720,"isCustomTemplate":false,"startTime":"2022-03-09T09:32:45.802Z","enableMediaPackage":false,"jobTemplate":"frogo1_Ott_720p_Avc_Aac_16x9_qvbr","enableSns":true,"srcVideo":"public/frog/android/video/223920131265.mp4","srcHeight":1280,"endTime":"2022-03-09T09:33:03.125Z","hlsPlaylist":"s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/hls/223920131265.m3u8","hlsUrl":"https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/hls/223920131265.m3u8","mp4Outputs":["s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.mp4","s3://frogo1-destination-otp4l535tez/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.0000001.jpg"],"mp4Urls":["https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.mp4","https://d4egpzynfumwb.cloudfront.net/e7faceb6-1d7f-4c15-8a21-368e08ef1687/mp4/223920131265.0000001.jpg"],"guid":"e7faceb6-1d7f-4c15-8a21-368e08ef1687"},"Timestamp":"2022-03-09T09:33:04.041Z","SignatureVersion":"1","Signature":"DMSxW8w3C+rhPrfpNwb0UBhd5IP2nxxKjfc0zUzD897/iR1GwqwTDx75nDUV1KMbqiKI14m70r1ureDp2lsIl/kakQda+fMXMXRAvIh/308czTnHAVsGWN5e0T2xFn7crgLdAEgGIcTlFqYgWb2JeC36OsM93rc2EU2h5ALOtN6D/XLagszFZWn0ljNAC0jtD3dbapyNkL4hqssUKSsfCVRTNFJaqDabcrH2yM3Iv/YAbhXuk8GbyETuGvSxswfu0bx/v0fMLvaDQsXVs2QJm/6XoAtUyXvim1zoO1Za3mdHIFcQbYvkhSY771kroSaWdpuBeZ3nFXwGDt+m8Ry+6g==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:frogo1-SnsTopic-5VHIY5478B4U:4dc1cf81-0065-4f88-a185-be3b037e5937"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def facerecognitionstart(self):
        """人脸识别开始"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/facerecognition/start'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"c336e7f0-fbad-52c8-bbc6-bd52381c56bc","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_FaceRecognition_end","Message":{"faceDateUrl":"https://d1476cpxvmnr6h.cloudfront.net/public/frog/faceData/164683809939923650_58912612.face","secretStr":"5f5591c852be8ee8e227242b81179ce2","timestamp":1646838129873,"videoId":58912612,"videoUrl":"https://d4egpzynfumwb.cloudfront.net/b972fdcd-34e0-4cc5-be94-37d275fc155d/mp4/iOS_TXUGC_20220309_1646838070228.mp4"},"Timestamp":"2022-03-09T15:02:09.958Z","SignatureVersion":"1","Signature":"UUU9Qoloc9xcdPItb0250gKDjJMXv53u5740OKyKpXHzpmow95yI6MbjLN4D19ib0vBKiRaZ7r7yWVzRSLzh3XLszhEUbRxceuWTp4oBTyHbjgXlKRdAVb/qt1R6vQAGsX97dIU+ffCqci3jjuVMiqbDArTIbFztjpvKja9E83Eguhl9vYcf/ZYMIhH49cR89BPqcHp+zCqa0Wvul5RLunYhMEDHHja8Fc6ButBo/M7973vlEsVVgYwFS5fQ2saMIbcTjXxTjgLcOYUypiKk2bUI2Hcw5ZjMvTbw+Hf+nN+USJSpAp3ZRu7ZAjEE0SLllUZNWPl5cpbxaXFF1WqyWQ==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_FaceRecognition_end:b5b91d69-f718-4e15-911f-ac3983f690d0"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def facerecognitionend(self):
        """人脸识别结束"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/facerecognition/end'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"c336e7f0-fbad-52c8-bbc6-bd52381c56bc","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_FaceRecognition_end","Message":{"faceDateUrl":"https://d1476cpxvmnr6h.cloudfront.net/public/frog/faceData/164683809939923650_58912612.face","secretStr":"5f5591c852be8ee8e227242b81179ce2","timestamp":1646838129873,"videoId":58912612,"videoUrl":"https://d4egpzynfumwb.cloudfront.net/b972fdcd-34e0-4cc5-be94-37d275fc155d/mp4/iOS_TXUGC_20220309_1646838070228.mp4"},"Timestamp":"2022-03-09T15:02:09.958Z","SignatureVersion":"1","Signature":"UUU9Qoloc9xcdPItb0250gKDjJMXv53u5740OKyKpXHzpmow95yI6MbjLN4D19ib0vBKiRaZ7r7yWVzRSLzh3XLszhEUbRxceuWTp4oBTyHbjgXlKRdAVb/qt1R6vQAGsX97dIU+ffCqci3jjuVMiqbDArTIbFztjpvKja9E83Eguhl9vYcf/ZYMIhH49cR89BPqcHp+zCqa0Wvul5RLunYhMEDHHja8Fc6ButBo/M7973vlEsVVgYwFS5fQ2saMIbcTjXxTjgLcOYUypiKk2bUI2Hcw5ZjMvTbw+Hf+nN+USJSpAp3ZRu7ZAjEE0SLllUZNWPl5cpbxaXFF1WqyWQ==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_FaceRecognition_end:b5b91d69-f718-4e15-911f-ac3983f690d0"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videoverifystart(self):
        """视频审核开始"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videoverify/start'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"9989d77e-8bf1-546b-8237-8ddc3ac257dc","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_Rekognition_start","Message":{"bucket":"amplify-frogandroiden-dev-181449-deployment181449-dev","S3ObjectName":"public/frog/android/video/2239214234325.mp4","videoId":69373676,"JobId":"482a78964b0a31db4fcccb5a44111b913f1cc8741ba6c72e9931d6114b1ccf73"},"Timestamp":"2022-03-09T13:43:15.273Z","SignatureVersion":"1","Signature":"gH6hLBXbS1R/lEX0ixJA/vYBG3HQWngvDqFFonYHq4aUsXA+4i3FjjTDTN4bPpAKSN1Hz/4wWglZOUcN0slNnU8ufKHSAlR0iHEhYSsz5vfSfjq//yzQF70fc3AGiKLPwRXFgVuMIzshFmXYZz5Y8MiKQiRhP0H6SXuh8GBXZ30rmbVM9OYGm+x2xs9anwnorOtFq38rltWwDHtrwt0oEA9iFApIHjCuOlBs5BsQvTVw3rf/eRx9m4SHJArtmbZmS//ZKB12kSHXKfrtxPcK72rHLmjny2ShlEoIq9tRJwOk+EpaeAX/IsbjvPASvT/Imx6BtyV97sVCgy5Hn9ZK+g==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_Rekognition_start:9e852c6e-99a6-4715-85dc-46200b53e6af"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))

    @task
    def videoverifystart(self):
        """视频审核结束"""
        url = 'http://test-vla.frogcool.com/videoFrogLogTask/v1/api/log/videoverify/end'
        h = {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification"
            }
        d = '{"Type":"Notification","MessageId":"9989d77e-8bf1-546b-8237-8ddc3ac257dc","TopicArn":"arn:aws:sns:us-east-1:071094189941:test_video_Rekognition_start","Message":{"bucket":"amplify-frogandroiden-dev-181449-deployment181449-dev","S3ObjectName":"public/frog/android/video/2239214234325.mp4","videoId":69373676,"JobId":"482a78964b0a31db4fcccb5a44111b913f1cc8741ba6c72e9931d6114b1ccf73"},"Timestamp":"2022-03-09T13:43:15.273Z","SignatureVersion":"1","Signature":"gH6hLBXbS1R/lEX0ixJA/vYBG3HQWngvDqFFonYHq4aUsXA+4i3FjjTDTN4bPpAKSN1Hz/4wWglZOUcN0slNnU8ufKHSAlR0iHEhYSsz5vfSfjq//yzQF70fc3AGiKLPwRXFgVuMIzshFmXYZz5Y8MiKQiRhP0H6SXuh8GBXZ30rmbVM9OYGm+x2xs9anwnorOtFq38rltWwDHtrwt0oEA9iFApIHjCuOlBs5BsQvTVw3rf/eRx9m4SHJArtmbZmS//ZKB12kSHXKfrtxPcK72rHLmjny2ShlEoIq9tRJwOk+EpaeAX/IsbjvPASvT/Imx6BtyV97sVCgy5Hn9ZK+g==","SigningCertURL":"https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem","UnsubscribeURL":"https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:071094189941:test_video_Rekognition_start:9e852c6e-99a6-4715-85dc-46200b53e6af"}'
        with self.client.post(url, data=d, headers=h, catch_response=True) as res:
            if res.status_code == 200:
                body = res.json()
                if body["code"] == 0:
                    res.success()
                else:
                    res.failure('message:{}'.format(body["message"]))
            else:
                res.failure('Failured:{}'.format(res.status_code))


class MyTeskGroup(HttpUser):
    """ 定义线程组 """
    tasks = [LoginTaskSet]



if __name__ == "__main__":
    # 单进程执行测试
    os.system('locust -f video_asynchronous_logs.py --web-host="127.0.0.1" --host=https://test.frogcool.com')