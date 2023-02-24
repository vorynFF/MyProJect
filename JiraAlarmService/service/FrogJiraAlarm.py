"""
@Project ：FrogApiAutoTest
@File    ：YmlUtil.py
@IDE     ：PyCharm
@Author  ：wuhaibo
@Date    ：2023/02/03 13:04 下午
"""

from jira.client import JIRA
from config.JiraYmlConfig import JiraYmlConfig

jiraConfig = JiraYmlConfig().get["jira"]


class FrogJira:
    def __init__(self, url, username, password) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.jiraLogin = None
        self.login_jira(self.url, self.username, self.password)

    def login_jira(self, url, username, password):
        login = JIRA(server=url, basic_auth=(username, password), options={'verify': False})
        self.jiraLogin = login
        return login

    # 问题的描述
    def get_all_fields(self):
        return self.jiraLogin.fields()

    # 获取问题工作流
    def get_transitions(self, issue):
        return self.jiraLogin.transitions(issue)

    # 获取活动日志
    def get_worklogs(self, issue):
        return self.jiraLogin.worklogs(issue)

    def get_project(self, projectId):
        return self.jiraLogin.project(id=projectId)

    def get_project_versions(self, project):
        return self.jiraLogin.project_versions(project)

    # 获取版本发布时间
    def get_edition(self, edition):
        version = self.jiraLogin.version(edition, expand="StartDate")
        return version.startDate

    def issue(self, issue_key):
        return self.jiraLogin.issue(issue_key)

    # jql
    def search_issue(self, jql, max_result=-1, **kw):
        search_result = self.jiraLogin.search_issues(jql, maxResults=max_result, **kw)
        return search_result

    def search_all_issue(self, jql, count=1000, **kw):
        startAt = 0
        page = 1
        sr = []
        sr_set = self.search_issue(jql, startAt=startAt, max_result=count, **kw)
        sr.extend(sr_set)
        print(f">>>>>>>>page count: {page}, total count: {len(sr)}, start at: {startAt}<<<<<<<<")
        while len(sr_set) == count:
            startAt = page * count
            sr_set = self.search_issue(jql, startAt=startAt, max_result=count, **kw)
            sr.extend(sr_set)
            page += 1
            print(f">>>>>>>>page count: {page}, total count: {len(sr)}, start at: {startAt}<<<<<<<<")
        return sr

