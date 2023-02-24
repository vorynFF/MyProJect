"""
@Project ：FrogApiAutoTest
@File    ：YmlUtil.py
@IDE     ：PyCharm
@Author  ：wuhaibo
@Date    ：2023/02/03 13:04 下午
"""

from config.JiraYmlConfig import JiraYmlConfig
from service.FrogJiraAlarm import FrogJira
from service.FrogWebHook import WebHook

jiraConfig = JiraYmlConfig().get["jira"]
webHookConfig = JiraYmlConfig().get["enterprise_weChat"]


def jiraMain():
    jira = FrogJira(jiraConfig['url'], jiraConfig['username'], jiraConfig['password'])
    frogProjects = jiraConfig['frogProjects']

    for project in frogProjects:

        url = webHookConfig[project + "_webhook_url"]

        jira.get_project(project)

        versions = jira.get_project_versions(project)

        if len(versions) == 0:
            raise Exception("Please add project version！")

        # 获取最近一个版本号的id
        versionId = versions[-1].id

        # 获取版本的创建时间
        versionTime = jira.get_edition(versionId)

        # 查询当前项目中所有的bug
        bug_all_sql = f'project = {project} AND created >= {versionTime} AND type = Bug order by created DESC'

        # 查询当前项目中所有的bug
        resolved_bug_sql = f'project = {project} AND created >= {versionTime} AND type = Bug AND status in ("已解决",' \
                           f'已关闭)  order by created DESC '

        # 查询当前项目中未完成的bug
        unresolved_bug_sql = f'project = {project} AND created >= {versionTime} AND type = Bug AND status in ("新建",' \
                             f'"重新激活","处理中")  order by created DESC '

        bugAll = jira.search_issue(bug_all_sql)
        resolvedBugsIdList = jira.search_issue(resolved_bug_sql)
        unresolvedBugsIdList = jira.search_all_issue(unresolved_bug_sql)
        unresolvedLinkAddressList = []

        for unresolvedBugId in unresolvedBugsIdList:
            # unresolvedLinkAddressList.append('http://jira.frogcool.com/browse/' + str(unresolvedBugId) +
            #                                  "，经办人: " + str(unresolvedBugId.fields.assignee))
            unresolvedLinkAddressList.append('[http://jira.frogcool.com/browse/' + str(unresolvedBugId) +
                                             "，经办人: " + str(unresolvedBugId.fields.assignee) + '](' + 'http://jira.frogcool.com/browse/' + str(unresolvedBugId)+')')

        unresolvedLink = ','.join(unresolvedLinkAddressList).replace(',', f'\n')
        content = f"**各位大佬，到目前为止<font color='blue'>{project}</font>项目的<font color='blue'>{versions[-1]}" \
                  f"</font>版本中缺陷修复情况,请查收！**\n" \
                  f"截至目前项目总共缺陷数: <font color='blue'>{bugAll.total}</font>**\n" \
                  f"截至目前已修复缺陷数: <font color='green'>{resolvedBugsIdList.total}</font>*\n" \
                  f"剩余未修复完缺陷数: <font color='red'>{len(unresolvedLinkAddressList)}</font>**\n" \
                  f"=====待研发修复详情如下=====\n" \
                  f"{unresolvedLink}"

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }

        webHook = WebHook(url)
        webHook.send_message(data)


if __name__ == '__main__':
    jiraMain()
