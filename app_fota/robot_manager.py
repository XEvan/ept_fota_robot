"""
    测试用例执行前后
"""
from app_fota.constants import Constants
from aw_lib.aw_manager import AwManager
from logger import rfic_info


def start():
    """
    所有测试用例执行之前执行的功能
    :return:
    """
    rfic_info("------start------")


def stop():
    """
    所有测试用例执行结束之后执行的功能
    :return:
    """
    rfic_info("------stop------")


def ota_task_deploy():
    """
    部署OTA云端任务
    :return:
    """
    return True


def setup():
    rfic_info("------setup------")
    AwManager.xldriver_channelbased_can_manager.reset()
    ota_task_deploy()  # 每条用例之前部署云端任务


def teardown():
    rfic_info("------teardown------")
    Constants.clean()  # 重置全局变量


def fota_assert(meas_status, expected_status, msg=""):
    """
    对结果做出判定
    如果"实际结果值"="预期结果值"，则成功，否则失败
    :param status1: 实际结果值
    :param status2: 预期结果值
    :param msg: 错误消息
    :return:
    """
    if str(meas_status) == str(expected_status):
        assert True, msg
    else:
        assert False, msg
