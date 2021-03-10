from logger import rfic_info

"""
    FOTA任务获取
"""


def fota_update_status_req():
    """
    FOTA_UpdateStatusReq
    车端上报升级任务状态
    请求方向：车->云
    :return: 返回解析出来的消息
    """
    rfic_info("等待ICC发送FOTA_UpdateStatusReq。。。")
    return True, ""

def fota_update_status_req_update_state_judge(meas_val, exp_val):
    """
    对FOTA_UpdateStatusReq消息中的fotaTaskStatus.updateState与期望值进行判断
    传进来的值是字符串形式，需要转换
    :param meas_val:
    :param exp_val:
    :return:
    """
    # meas_val = int(meas_val, 16)  # 都转换成十进制，方便比较
    # exp_val = int(exp_val, 16)  # 都转换成十进制，方便比较
    if meas_val == exp_val:
        assert True, ""
    else:
        assert False, "update state not match[meas=%s][expected=%s]" % (str(meas_val), str(exp_val))

def fota_update_status_resp():
    """
    FOTA_UpdateStatusResp
    云端反馈收到任务上报状态信息
    请求方向：云->车
    :return:
    """
    rfic_info("等待OTA后台发送FOTA_UpdateStatusResp。。。")
    return True, ""


