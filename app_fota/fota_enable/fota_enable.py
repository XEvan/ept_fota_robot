import random

from app_fota.hw_handles import XLDriverHandles

"""
    FOTA使能
"""


def fota_function_enable_configuration(enable=True):
    """
    获取FOTA功能使能配置字字段配置
    :param enable: True:有效  False:无效
    :return:
    """
    id = 0xC910
    return True


def vin_validate(status=True):
    """
    ICC存储的VIN与BCM通过CAN总线发送的VIN一致性校验
    :param enable: True:一致  False:不一致
    :return:
    """
    # ICC的VIN码：F190
    # 车辆VIN不匹配(BCM&ICC)：D500
    id = 0x500
    return True


def security_vehicle_identification_certificate_status(status=True):
    """
    车辆身份证书获取状态
    :param enable: True:已获取  False:为获取
    :return:
    """
    id = 0xACC1
    return True


def sys_pwr_mode(mode="off"):
    """
    设置系统电源模式SysPwrMd
    :param mode: off->OFF, no_off->非OFF
    :return:
    """
    return True
