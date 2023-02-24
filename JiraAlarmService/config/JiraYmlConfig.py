"""
@Project ：FrogApiAutoTest
@File    ：YmlUtil.py
@IDE     ：PyCharm
@Author  ：wuhaibo
@Date    ：2022/06/28 13:04 下午
"""
import os.path
import yaml


class JiraYmlConfig:
    def __init__(self, path=None):
        if path:
            self.path = path
        else:
            self.path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'jiraConfig.yml')

    @property
    def get(self):
        with open(self.path, "r", encoding="utf-8") as yml:
            return yaml.safe_load(yml.read())
