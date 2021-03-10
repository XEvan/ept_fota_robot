"""
    FOTA使能
"""
from aw_lib.aw_manager import AwManager


def network_access(enable=True):
    return True


def fota_function_enable_configuration(enable=True):
    """
    获取FOTA功能使能配置字字段配置
    CANID：0x710
    dlc设置为5
    DATA：04 2E C9 10 C0
    最后一个字节：
        C0:有效
        40:无效
    :param enable: True:有效  False:无效
    :return:
    """
    enable = eval(str(enable))

    can_id = 0x710
    if enable:
        data = [0x04, 0x2E, 0xC9, 0x10, 0xC0]
    else:
        data = [0x04, 0x2E, 0xC9, 0x10, 0x40]
    AwManager.xldriver_channelbased_can_manager.can_send_in_single(can_id, data, expected_can_id=0x718)
    return True


def vin_validate(status=True):
    """
    ICC存储的VIN与BCM通过CAN总线发送的VIN一致性校验
    :param enable: True:一致  False:不一致
    :return:
    """
    status = eval(str(status))
    # ICC的VIN码：F190
    # 车辆VIN不匹配(BCM&ICC)：D500
    return True


def security_vehicle_identification_certificate_status(status=True):
    """
    设置车辆身份证书未获取：
        CANID：0x710
        DATA：04 2E B9 33 00
    设置车辆身份证书获取：
        CANID：0x710
        DATA：04 2E B9 33 01
    :param enable: True:已获取  False:为获取
    :return:
    """
    status = eval(str(status))

    can_id = 0x710
    if status:
        data = [0x04, 0x2E, 0xB9, 0x33, 0x01]
    else:
        data = [0x04, 0x2E, 0xC9, 0x10, 0x00]
    AwManager.xldriver_channelbased_can_manager.can_send_in_single(can_id, data, expected_can_id=0x718)
    return True


def sys_pwr_mode(mode="off"):
    """
    设置系统电源模式SysPwrMd
    :param mode: off->OFF, no_off->非OFF
    :return:
    """
    return True


def fota_enable_precondition(network=True, conf=True, vin=True, cert=True):
    """
    FOTA使能前提条件
    :param network: 网络是否可访问，默认可访问
    :param conf:  配置字是否可有效，默认有效
    :param vin:  VIN是否一致，默认一致
    :param cert:  身份证书是否已获取，默认已获取
    :return:
    """
    network_access(eval(str(network)))  # 外网是否可访问
    fota_function_enable_configuration(eval(str(conf)))  # 配置字是否有效
    vin_validate(eval(str(vin)))  # VIN是否一致
    security_vehicle_identification_certificate_status(eval(str(cert)))  # 身份证书是否已获取
