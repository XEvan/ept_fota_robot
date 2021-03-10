from logger import rfic_info

"""
    FOTA日志上传
"""


def fota_get_log_upload_url_req():
    """
    FOTA_GetLogUploadURLReq
    请求方向：ICC->IAM
    :return: 返回解析出来的消息
    """
    rfic_info("等待ICC发送FOTA_GetLogUploadURLReq。。。")
    return True, ""


def fota_get_log_upload_url_resp():
    """
    FOTA_GetLogUploadURLResp
    请求方向：IAM->ICC
    :return: 返回解析出来的消息
    """
    rfic_info("等待IAM发送FOTA_GetLogUploadURLResp。。。")
    return True, ""


def fota_report_upload_log_result_req():
    """
    FOTA_ReportUploadLogResultReq
    请求方向：ICC->IAM
    :return: 返回解析出来的消息
    """
    rfic_info("等待ICC发送FOTA_ReportUploadLogResultReq。。。")
    return True, ""


def fota_report_upload_log_result_resp():
    """
    FOTA_ReportUploadLogResultResp
    请求方向：IAM->ICC
    :return: 返回解析出来的消息
    """
    rfic_info("等待IAM发送FOTA_ReportUploadLogResultResp。。。")
    return True, ""


def fota_report_upload_log_result_resp_status_code_judge(meas_val, exp_val):
    """
    对FOTA_ReportUploadLogResultResp消息中的responseInfo.statusCode与期望值进行判断
    传进来的值是字符串形式，需要转换
    :param meas_val:
    :param exp_val:
    :return:
    """
    if meas_val == exp_val:
        assert True, ""
    else:
        assert False, "report_upload_log status code not match[meas=%s][expected=%s]" % (str(meas_val), str(exp_val))
