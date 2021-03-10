import time

from app_fota.constants import Constants
from logger import rfic_info

"""
    车辆数据上传
"""


def fota_triggersession(expected_trigger_type="GetLogistics", timeout=1):
    """
    FOTA_TriggerSession
    云端发起，主动向车端触发某个流程， 此请求无对应的响应消息
    车端根据自身状态来执行消息中期望的流程
    请求方向：云->车
    :param trigger_type: 触发类型
    :param timeout: 超时时间，默认30s
    :return:
    """
    rfic_info("检测OTA后台发送FOTA_TriggerSession。。。")

    # 检测并解析报文
    current_time = time.time()  # 开始检测的时间点
    while time.time() - current_time <= timeout:
        # 检测报文

        requestInfo = {}
        triggerInfo = {}

        # 明确消息 requestInfo.requestMethod="FOTA_TriggerSession"
        condition1 = requestInfo.get("requestMethod") == "FOTA_TriggerSession"
        # 检测到报文
        if condition1:
            # 触发类型=指定的trigger_type
            trigger_type = triggerInfo.get("type")
            condition2 = trigger_type == expected_trigger_type
            # 检测到报文且报文的triggerType为指定type
            if condition2:
                request_id = requestInfo.get("requestId", None)
                Constants.request_id = request_id
                rfic_info("检测到云端报文：FOTA_TriggerSession, requestId=[%s]" % str(request_id))
                return True, ""
            else:
                return False, "检测到云端报文：FOTA_TriggerSession，[解析的type][%s]!=[期望的type][%s]" % (
                    str(trigger_type), str(expected_trigger_type))
    return False, "超时[%ss]未检测到云端报文：FOTA_TriggerSession" % str(timeout)


def fota_get_logistics_manifest_req(timeout=1):
    """
    FOTA_GetLogisticsManifestReq
    车端向云端获取最新物流文件定义(云端解析A2文件内容)
    请求方向：车->云
    :return:
    """
    rfic_info("等待ICC给OTA后台发送FOTA_GetLogisticsManifestReq。。。")

    # 检测并解析报文
    current_time = time.time()  # 开始检测的时间点
    while time.time() - current_time <= timeout:
        # 检测报文

        requestInfo = {}
        triggerInfo = {}

        # 明确消息 requestInfo.requestMethod="FOTA_GetLogisticsManifestReq"
        condition1 = requestInfo.get("requestMethod") == "FOTA_GetLogisticsManifestReq"
        # 检测到报文
        if condition1:
            # 云端触发：
            #   报文中有requestId, Constants.request_id也有值(triggerSession的requestId)，两者正常情况下一致
            # 车端触发
            #   报文中有requestId, Constants.request_id为None
            if Constants.request_id is None:
                # 车端触发,Constants.request_id=None,无需比对
                return True, ""
            else:
                # 云端触发,Constants.request_id来自于FOTA_TriggerSession,两者正常情况下一致
                request_id = requestInfo.get("requestId")
                condition2 = request_id == Constants.request_id
                return condition2, ""
    return False, "超时[%ss]未检测到车端报文：FOTA_GetLogisticsManifestReq" % str(timeout)


def fota_get_logistics_manifest_resp(timeout=1):
    """
    FOTA_GetLogisticsManifestResp
    车端向云端获取最新物流文件定义(云端解析A2文件内容)
    请求方向：云->车
    :return: 成功则返回解析好的字段
    """
    rfic_info("等待OTA后台发送FOTA_GetLogisticsManifestResp。。。")

    # 检测并解析报文
    current_time = time.time()  # 开始检测的时间点
    while time.time() - current_time <= timeout:
        # 检测报文

        requestInfo = {}
        triggerInfo = {}

        # 明确消息 requestInfo.requestMethod="FOTA_GetLogisticsManifestResp"
        condition1 = requestInfo.get("requestMethod") == "FOTA_GetLogisticsManifestResp"
        # 检测到报文
        if condition1:
            return True, ""
    return False, "超时[%ss]未检测到云端报文：FOTA_GetLogisticsManifestResp" % str(timeout)


def fota_check_version_req(timeout=1):
    """
    FOTA_CheckVersionReq
    车端上报物流信息，并请求云端是否有FOTA任务
    请求方向：车->云
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_CheckVersionReq。。。")

    # 检测并解析报文
    current_time = time.time()  # 开始检测的时间点
    while time.time() - current_time <= timeout:
        # 检测报文

        requestInfo = {}
        triggerInfo = {}

        # 明确消息 requestInfo.requestMethod="FOTA_CheckVersionReq"
        condition1 = requestInfo.get("requestMethod") == "FOTA_CheckVersionReq"
        # 检测到报文
        if condition1:
            return True, ""
    return False, "超时[%ss]未检测到车端报文：FOTA_CheckVersionReq" % str(timeout)


def fota_check_version_resp(timeout=1):
    """
    FOTA_CheckVersionResp
    云端反馈物流数据上报后处理结果，如果有升级任务，则同时下发
    请求方向：云->车
    :return: 返回解析的结果
    """
    rfic_info("等待OTA后台发送FOTA_CheckVersionResp。。。")

    # 检测并解析报文
    current_time = time.time()  # 开始检测的时间点
    while time.time() - current_time <= timeout:
        # 检测报文

        requestInfo = {}
        triggerInfo = {}

        # 明确消息 requestInfo.requestMethod="FOTA_CheckVersionResp"
        condition1 = requestInfo.get("requestMethod") == "FOTA_CheckVersionResp"
        # 检测到报文
        if condition1:
            return True, ""
    return False, "超时[%ss]未检测到云端报文：FOTA_CheckVersionResp" % str(timeout)


def check_version_resp_update_mode_judge(meas_val, exp_val):
    """
    对FOTA_CheckVersionResp消息中的fotaTaskInfo.updMode与期望值进行判断
    传进来的值是字符串形式，需要转换
    :param meas_val:
    :param exp_val:
    :return:
    """
    if meas_val == exp_val:
        assert True, ""
    else:
        assert False, "update mode not match[meas=%s][expected=%s]" % (str(meas_val), str(exp_val))


def firewall_certificate_config(status=True):
    """
    配置防火墙认证状态
    :param status: True则成功，False则失败
    :return:
    """
    status = eval(str(status))
    return True


def disconnect_ecu(src_ecu_name="IAM", dst_ecu_nam="ICC"):
    """
    断开指定ECU
    :param src_ecu_name: 源ECU
    :param dst_ecu_name: 目的ECU
    :return:
    """
    return True


def simulation_message(src_ecu_name="IAM", dst_ecu_name="ICC", message_type="error_mnf_info"):
    """
    仿真报文
    :param src_ecu_name: 源ECU
    :param dst_ecu_name: 目的ECU
    :param message_type: 内置消息类型，根据消息类型去执行不同的逻辑
    :return:
    """
    if message_type == "error_mnf_info":
        return True, ""
    return False, "Error"
