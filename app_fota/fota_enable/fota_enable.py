"""
    FOTA使能
"""
from aw_lib.aw_manager import AwManager


def network_access(enable=True):
    """
    串口通信
        开启：route add default 172.31.8.18
        开启默认网关：route add default 172.31.8.18
        关闭:  route del default
    :param enable:
    :return:
    """
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
    AwManager.xldriver_channelbased_can_manager.can_send_single_frame(can_id, data, expected_can_id=0x718)
    return True


def vin_validate(status=True):
    """
    ICC存储的VIN与BCM通过CAN总线发送的VIN一致性校验
    VIN的设置，
        CANID：0x710
        DID:F190
        DATA：17byte（VIN码）需要用连续帧去发。
    :param enable: True:一致  False:不一致
    :return:
    """
    status = eval(str(status))
    can_id = 0x710
    sid = 0x2E  # ?
    did = 0xF190
    data = []
    AwManager.xldriver_channelbased_can_manager.can_send_multi_frame(can_id, sid, did, data, expected_can_id=0x718)
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
    AwManager.xldriver_channelbased_can_manager.can_send_single_frame(can_id, data, expected_can_id=0x718)
    return True


def sys_pwr_mode(mode="off"):
    """
    设置系统电源模式SysPwrMd
    :param mode: off->OFF, no_off->非OFF
    :return:
    """
    return True, ""


def fota_enable_success(network=True, conf=True, vin=True, cert=True):
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


def diagnosis_config(monitor_enable=True, access_status=True):
    """
    配置：
        ①诊断OBD诊断设备的DID监控使能状态
        ②诊断仪接入状态
    :param monitor_enable: 监控使能状态，True表示监控使能
    :param access_status: 诊断仪接入状态，True表示已接入
    :return:
    """
    monitor_enable = eval(str(monitor_enable))
    access_status = eval(str(access_status))
    return True


def vehicle_sleep(enable=True):
    """
    设置车辆休眠
    @:param enable: True表示设置车辆休眠
    :return:
    """