# from app_fota.hw_handles import XLDriverHandles

"""
    硬件的初始化
"""


def hw_setup():
    """
    硬件初始化，VN5640对CAN、ETH的配置（包括连接）
    :return:
    """
    pass
    # XLDriverHandles.xldriver_can_handle.reset()  # CAN的配置
    # XLDriverHandles.xldriver_eth_handle.reset()  # ETH的配置


def hw_teardown():
    """
    硬件teardown
    :return:
    """
    pass
    # XLDriverHandles.xldriver_eth_handle.cleanup()


def hello(a=1, b=2):
    print("a:", a)
    print("b:", b)
    if eval(b):
        print("=======")
    return True, "123"
