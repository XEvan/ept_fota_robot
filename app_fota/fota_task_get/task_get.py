from logger import rfic_info

"""
    FOTA任务获取
"""


def fota_update_status_req():
    """
    FOTA_UpdateStatusReq
    车端上报升级任务状态
    请求方向：车->云
    :return:
    """
    rfic_info("等待ICC发送FOTA_UpdateStatusReq。。。")


def fota_update_status_resp():
    """
    FOTA_UpdateStatusResp
    云端反馈收到任务上报状态信息
    请求方向：云->车
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_UpdateStatusResp。。。")
