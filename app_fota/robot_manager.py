"""
    测试用例执行前后
"""
from app_fota.constants import Constants
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


def setup():
    rfic_info("------setup------")


def teardown():
    rfic_info("------teardown------")
    Constants.clean() # 重置全局变量
