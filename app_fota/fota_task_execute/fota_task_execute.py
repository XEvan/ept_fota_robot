from logger import rfic_info

"""
    FOTA任务执行
"""


def fota_hmi_status():
    """
    FOTA_HMIStatus
    请求方向：ICC->ICM
    :return: 返回解析出来的消息
    """
    rfic_info("等待ICC发送FOTA_HMIStatus。。。")
    return True, ""

def fota_hmi_status_update_mode_judge(meas_val, exp_val):
    if meas_val == exp_val:
        assert True, ""
    else:
        assert False, "fota_hmi_status update mode not match[meas=%s][expected=%s]" % (str(meas_val), str(exp_val))

def fota_hmi_update_progress():
    """
    FOTA_HMIUpdateProgress
    请求方向：ICC->ICM
    :return: 返回解析出来的消息
    """
    rfic_info("等待ICC发送FOTA_HMIUpdateProgress。。。")
    return True, ""


def fota_hmi_update_progress_update_status_judge(meas_val, exp_val):
    if meas_val == exp_val:
        assert True, ""
    else:
        assert False, "fota_hmi_update_progress_update_status not match[meas=%s][expected=%s]" % (str(meas_val), str(exp_val))
