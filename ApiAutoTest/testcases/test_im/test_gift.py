"""
@Project ：PyCharm
@File    ：test_gift.py
@IDE     ：PyCharm
@Author  ：wuhaibo
@Date    ：2022/06/23
"""
import logging

from common.FrogHeader import FrogHeader
from common.FrogRequest import frog_req
from config.FrogConf import frog
from db.FrogSSHMysqlHandle import MysqlHandle
from utils.Loggers import Loggers
from testcases.FrogLogin import login_whb
from utils.YmlUtil import ymlUtil

logger = Loggers()
yml = ymlUtil().get["frog"]['api']['im']['gift']
con = MysqlHandle()


class TestGift:
    # 获取礼物列表接口
    def test_getPurchasedGiftsListV2(self, login_whb):
        url = frog["host"] + yml['getPurchasedGiftsListV2Api']
        res = frog_req.post(url, headers=login_whb)
        logger.info("getPurchasedGiftsListV2:{}".format(res))
        assert res["body"]["state"]["msg"] == "Operation succeeded;Operation succeeded"

    # 送礼物可兑换的礼物列表接口
    def test_getGiftInfoList(self, login_whb):
        url = frog["host"] + yml['getGiftInfoListApi']
        data = {"queryType": "v1_gift"}
        res = frog_req.post(url, json=data, headers=login_whb)
        logger.info("getGiftInfoList:{}".format(res))

        assert res["body"]["state"]["msg"] == "get successful;get successful"

    # 批量送礼物接口
    def test_givingGiftsV2(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['givingGiftsV2Api']
        logger.info("=========批量IM赠送免费礼物逻辑测试=========")

        gift_im_data = {
            "giftId": 33,
            "friendUserId": "86724026",
            "videoId": "",
            "giftSize": 3
        }
        gift_im_res = frog_req.post(url, json=gift_im_data, headers=login_whb)
        logger.info("givingGiftsV2:{}".format(gift_im_res))
        assert gift_im_res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert gift_im_res['body']['data']['giftSize'] == '0'

        logger.info("=========批量赠送视频免费礼物逻辑测试=========")
        gift_video_data = {
            "giftId": 33,
            "friendUserId": "86724026",
            "videoId": "80737412",
            "giftSize": 3
        }

        gift_video_res = frog_req.post(url, json=gift_video_data, headers=login_whb)
        logger.info("givingGiftsV2:{}".format(gift_video_res))

        # 获取该user_id送该视频id礼物的总数
        give_video_gift_count_sql = "select " \
                                    "   count(*) " \
                                    "from " \
                                    "   gift_rec_info " \
                                    "where " \
                                    "   1=1 " \
                                    "and " \
                                    "   user_id = {} " \
                                    "and " \
                                    "   friend_user_id = {} " \
                                    "and " \
                                    "   video_id = {} ".format(header['userId'], gift_video_data['friendUserId'],
                                                               gift_video_data['videoId'])
        give_gift_count = con.select(give_video_gift_count_sql)
        assert gift_video_res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert int(gift_video_res['body']['data']['giftSize']) == int(give_gift_count[0][0])

        # 获取该user_id下对应的游泳圈数量
        get_balance_sum_sql = "select " \
                              "     *" \
                              " from  " \
                              "     user_gold_account  " \
                              "where user_id = {} " \
                              "ORDER BY " \
                              "     create_time desc;".format(header['userId'])
        balance_sum = con.select(get_balance_sum_sql)
        logger.info("=========判断该用户下的游泳圈数量是否大于0=========")
        assert int(balance_sum[0][1]) > 0

        logger.info("=========批量IM赠送付费礼物逻辑测试=========")
        pay_gift_im_data = {
            "giftId": 36,
            "friendUserId": "86724026",
            "videoId": "",
            "giftSize": 3
        }
        pay_gift_im_res = frog_req.post(url, json=pay_gift_im_data, headers=login_whb)
        logger.info("givingGiftsV2:{}".format(gift_im_res))
        assert pay_gift_im_res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert pay_gift_im_res['body']['data']['giftSize'] == '0'

        logger.info("=========批量视频赠送付费礼物逻辑测试=========")
        pay_gift_video_data = {
            "giftId": 36,
            "friendUserId": "86724026",
            "videoId": "80737412",
            "giftSize": 3
        }

        pay_gift_video_res = frog_req.post(url, json=pay_gift_video_data, headers=login_whb)
        logger.info("givingGiftsV2:{}".format(gift_im_res))
        assert pay_gift_video_res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert int(pay_gift_video_res['body']['data']['giftSize']) == \
               int(give_gift_count[0][0]) + pay_gift_video_data['giftSize']

    # 获取礼物榜列表接口
    def test_getFriendGiftBoostList(self, login_whb):
        header = login_whb
        url = frog["host"] + yml['getFriendGiftBoostListApi']
        data = {"friendUserId": 86724026}
        logger.info("获取礼物榜列表接口")
        res = frog_req.post(url, json=data, headers=header)
        logger.info("getFriendGiftBoostList:{}".format(res))
        assert res['body']['state']['msg'] == 'Operation succeeded;Operation succeeded'
        assert len(res['body']['data']['findRespVoList']) > 0

