from app_fota.hw_handles import XLDriverHandles


def hw_setup():
    """
    硬件初始化，VN5640对CAN、ETH的配置（包括连接）
    :return:
    """
    XLDriverHandles.xldriver_can_handle.reset()  # CAN的配置
    XLDriverHandles.xldriver_eth_handle.reset()  # ETH的配置


def hw_teardown():
    """
    硬件teardown
    :return:
    """
    XLDriverHandles.xldriver_eth_handle.cleanup()