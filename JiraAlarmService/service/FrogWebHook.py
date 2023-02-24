import requests


class WebHook:
    def __init__(self, url) -> None:
        self.url = url

    def send_message(self, message):
        reponse = requests.post(self.url, json=message)
        if reponse.json().get('errcode') != 0:
            raise Exception("Message sending failed！")
        return reponse.text

