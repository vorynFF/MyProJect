"""
@Project ：PyCharm
@File    ：test_explore.py
@IDE     ：PyCharm
@Author  ：wuhaibo
@Date    ：2022/10/29
"""
from common.FrogRequest import frog_req
from config.FrogConf import frog
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.Loggers import Loggers
from utils.YmlUtil import ymlUtil
from testcases.FrogLogin import login_whb

logger = Loggers()
con = MysqlHandle()
yml = ymlUtil().get["frog"]['api']['metab']['explore']

friendUserId = 86724026


class TestExplore:
    def test_getUserExplore(self, login_whb):
        header = login_whb
        print("header:{}".format(header))
        url = frog["host"] + yml['userExplore']
        data = {"friendUserId": friendUserId}
        logger.info("getUserExplore request data: {}".format(str(data)))
        res = frog_req.post(url, headers=header, json=data)
        logger.info("getUserExplore response: {}".format(res))
        assert 'Operation succeeded;Operation succeeded' == res['body']['state']['msg']
        assert res['body']['data'] != {}

    # def test_getChatExploreData(self, login_whb):
    #     header = login_whb
    #     print("header:{}".format(header))
    #     url = frog["host"] + yml['chatExploreData']
    #     print(url)
    #     data = {"friendUserId": friendUserId}
    #     logger.info("getChatExploreData request data: {}".format(str(data)))
    #     res = frog_req.post(url, headers=header, data=data)
    #     logger.info("getChatExploreData response: {}".format(res))
    #     assert 'Operation succeeded;Operation succeeded' == res['body']['state']['msg']
    #     assert res['body']['data'] != {}