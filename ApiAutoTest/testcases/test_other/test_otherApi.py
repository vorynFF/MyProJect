import time

from common.FrogRequest import frog_req
from config.FrogConf import frog
from testcases.FrogLogin import login_whb
from utils.Loggers import Loggers
from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['other']['otherApi']


class TestFrogOther:
    # 保存客户端开启和关闭时间
    def test_saveAppOnlineTime(self, login_whb):
        header = login_whb
        logger.info("保存客户端开启和关闭时间")
        url = frog["host"] + yml['saveAppOnlineTimeApi']
        data = {"userId": header['userId'], "appClientOpenTimeStamp": str(int(time.time()) - 60 * 60 * 2),
                "appClientCloseTimeStamp": str(int(time.time()))}
        res = frog_req.post(url, headers=header, json=data)
        logger.info("saveAppOnlineTime:{}".format(res))
        assert res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'

