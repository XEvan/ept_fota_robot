import random

from app_fota.hw_handles import XLDriverHandles
from logger import rfic_info


def start():
    """
    ①启动数据服务器
    :return:
    """
    print("------start------")


def stop():
    """
    ①停止数据服务器
    :return:
    """
    print("------stop------")


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
    data = [random.randint(0, 15) for i in range(0, 8)]
    XLDriverHandles.xldriver_can_handle.can_send_in_single(id, data)
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


def precondition():
    """
    ①FOTA功能使能配置字字段配置为有效
    ②ICC存储的VIN与BCM通过CAN总线发送的VIN一致
    ③ICC车辆身份证书状态为已获取
    :return:
    """
    conf_status = fota_function_enable_configuration()
    vin_status = vin_validate()
    sec_cer_status = security_vehicle_identification_certificate_status()

    assert conf_status is True
    assert vin_status is True
    assert sec_cer_status is True


def fota_triggersession(src="IAM", dst="ICC"):
    # 等待具体的消息过来后，开始进行消息的仿真发送
    rfic_info("等待OTA后台发送FOTA_TriggerSession。。。")
    return
    status, target_params = XLDriverHandles.xldriver_eth_handle.get_required_message(src, dst, 0x0100, 0x3b)
    rfic_info("收到期望消息:", str(target_params))


def fota_get_logistics_manifest_req(src="ICC", dst="IAM"):
    rfic_info("等待ICC给OTA后台发送FOTA_GetLogisticsManifestReq。。。")
    return
    status, target_params = XLDriverHandles.xldriver_eth_handle.get_required_message(src, dst, 0x0100, 0x3b)
    rfic_info("收到期望消息:", str(target_params))
