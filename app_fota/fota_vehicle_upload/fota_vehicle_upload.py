import time

from app_fota.constants import Constants
from app_fota.fota_enable.fota_enable import fota_enable_success, sys_pwr_mode
from app_fota.robot_manager import fota_assert
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

        res = {}

        # 明确消息 requestInfo.requestMethod="FOTA_GetLogisticsManifestReq"
        condition1 = res.get("requestMethod") == "FOTA_GetLogisticsManifestReq"
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
                request_id = res.get("requestId")
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


def fota_check_version_req(times=1, timeout=1):
    """
    FOTA_CheckVersionReq
    车端上报物流信息，并请求云端是否有FOTA任务
    请求方向：车->云
    @param times: 检测请求次数，默认1次
    :return: 解析出来的字典
    """
    res_list = []
    for _ in range(times):
        # 连续检测times次，
        rfic_info("等待OTA后台发送FOTA_CheckVersionReq。。。")

        # 检测并解析报文
        current_time = time.time()  # 开始检测的时间点
        res = False
        while time.time() - current_time <= timeout:
            # 检测报文

            requestInfo = {}
            triggerInfo = {}

            # 明确消息 requestInfo.requestMethod="FOTA_CheckVersionReq"
            condition1 = requestInfo.get("requestMethod") == "FOTA_CheckVersionReq"
            # 检测到报文
            if condition1:
                res = True
                break
        res_list.append(res)

    # 列表中的True的次数应该与times相等  -s
    true_cnt = 0
    for ele in res_list:
        if ele:
            true_cnt += 1
    # 列表中的True的次数应该与times相等  -e
    if true_cnt == times:
        return True, ""
    else:
        return False, "超时[%ss]未检测到车端报文[%s/%s]：FOTA_CheckVersionReq" % (str(timeout), true_cnt, times)


def result_dict_judge(meas_val, exp_val):
    """
    解析的结果与期望结果的判定是否一致
    逐级列出，以点号隔开，如：logisticsDatainfo.ecuNum=0
    :param meas_val: 解析出来的结果，字典形式的字符串
    :param exp_val: 预期结果，字典形式的字符串
        logisticsDatainfo.ecuNum=0
    :return:
    """
    meas_val = eval(str(meas_val))  # 字典格式，解析到的完整数据包
    keys_str, exp_val = str(exp_val).split("=")  # ["logisticsDatainfo.ecuNum", "0"]
    key_list = keys_str.split(".")

    for key in key_list:
        meas_val = meas_val.get(key, {})  # 不断迭代到对应的层级，获取最终的结果

    if str(meas_val) == str(exp_val):
        assert True, ""
    else:
        assert False, "%s的值不匹配, meas_v=[%s], exp_v=[%s]" % (keys_str, meas_val, exp_val)


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


def ecu_data_gain_status():
    """
    ECU物流数据收集状态
    :return: True表示收集完成
    """
    return True, ""


def vehicle_data_list_obtain_success(trigger_type="AUTO"):
    """
    获取车辆物流数据清单成功
    @:param trigger_type: 触发方式，默认车端自动触发(auto)，OTA平台触发(OTA)
    :return:
    """
    fota_enable_success()  # FOTA使能正常
    if trigger_type == "AUTO":
        status = sys_pwr_mode("no_off")  # 系统电源模式设为"非OFF"
    else:  # OTA触发
        status = fota_triggersession()  # 云端下发命令触发
    fota_assert(status[0], True, status[1])  # 期望结果是True

    status = fota_get_logistics_manifest_req()
    fota_assert(status[0], True, status[1])

    status = fota_get_logistics_manifest_resp()  # 获取到车辆物流数据清单
    fota_assert(status[0], True, status[1])  # 如果获取到了，则True，否则报错


def ecu_data_gain_success(trigger_type="AUTO"):
    """
    ECU物流数据收集完成
    :return:
    """
    vehicle_data_list_obtain_success(trigger_type)  # 获取车辆物流数据清单
    status = ecu_data_gain_status()
    fota_assert(status[0], True, status[1])  # 如果收集完成，则True，否则报错


def vehicle_data_upload_success(trigger_type="AUTO"):
    """
    车辆物流数据上传完成
    :return:
    """
    ecu_data_gain_success(trigger_type)  # ECU物流数据收集完成

    status = fota_check_version_req()
    fota_assert(status[0], True, status[1])
