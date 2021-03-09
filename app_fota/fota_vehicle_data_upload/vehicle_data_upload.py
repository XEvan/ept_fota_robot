from logger import rfic_info


def fota_triggersession():
    """
    FOTA_TriggerSession
    云端发起，主动向车端触发某个流程， 此请求无对应的响应消息
    车端根据自身状态来执行消息中期望的流程
    请求方向：云->车
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_TriggerSession。。。")


def fota_get_logistics_manifest_req():
    """
    FOTA_GetLogisticsManifestReq
    车端向云端获取最新物流文件定义(云端解析A2文件内容)
    请求方向：车->云
    :return:
    """
    rfic_info("等待ICC给OTA后台发送FOTA_GetLogisticsManifestReq。。。")


def fota_get_logistics_manifest_resp():
    """
    FOTA_GetLogisticsManifestResp
    车端向云端获取最新物流文件定义(云端解析A2文件内容)
    请求方向：云->车
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_GetLogisticsManifestResp。。。")


def fota_check_version_req():
    """
    FOTA_CheckVersionReq
    车端上报物流信息，并请求云端是否有FOTA任务
    请求方向：车->云
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_CheckVersionReq。。。")


def fota_check_version_resp():
    """
    FOTA_CheckVersionResp
    云端反馈物流数据上报后处理结果，如果有升级任务，则同时下发
    请求方向：云->车
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_CheckVersionResp。。。")
