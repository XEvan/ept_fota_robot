import time
from ctypes import byref, c_uint

import can
from can import Message
from can.interfaces.vector import VectorBus

from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.structures_tx import XLevent
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased import ChannelBased
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from logger import rfic_info


class ChannelBasedCanTx(ChannelBased):
    def __init__(self):
        super(ChannelBasedCanTx, self).__init__()

        self.validate_status = False  # 是否需要等待响应报文，False为不需要或者已经得到响应
        self.response = None

    # @Deprecated
    def can_send(self, canMask, xlEvent):
        pEventCount = c_uint(1)
        status = self.dll.xlCanTransmit(self.canPortHandle, canMask, byref(pEventCount), byref(xlEvent))
        rfic_info("can transmit:", status)

    # @Deprecated
    def generate_tx_data(self):
        xlEvent = XLevent()

        xlEvent.tag = ChannelBasedConstants.XL_TRANSMIT_MSG
        xlEvent.tagData.msg.id = 0x01
        xlEvent.tagData.msg.dlc = 8
        xlEvent.tagData.msg.flags = 0
        xlEvent.tagData.msg.data[0] = 1
        xlEvent.tagData.msg.data[1] = 2
        xlEvent.tagData.msg.data[2] = 3
        xlEvent.tagData.msg.data[3] = 4
        xlEvent.tagData.msg.data[4] = 5
        xlEvent.tagData.msg.data[5] = 6
        xlEvent.tagData.msg.data[6] = 7
        xlEvent.tagData.msg.data[7] = 8
        return xlEvent

    def rx_callback(self, msg):
        """
        分析总线上的报文信息
        :param msg:
        :return:
        """
        print(msg)
        self.validate_status = False  # 检测到期望报文
        self.response = msg

    def can_send_in_single(self, id, data, wait_ret=True, timeout=30):
        """
        单帧
        :param id: 发送的id
        :param data: 发送的数据
        :param wait_ret: 是否等待回复
        :return: 响应报文
        """
        self.validate_status = wait_ret  # 默认需要等待响应报文
        # 获取配置文件中的配置信息  -s
        canAppName = str(self.canAppName.value, encoding="utf-8")  # CAN Application的name
        channels = []  # 配置文件中的CAN相关的AppChannel
        for name, ch in self.canAppChannel.items():
            channels.append(ch["appChannel"])
        bitrate = 500000
        # 获取配置文件中的配置信息  -e

        # 回调，实例化RX VectorBus，接收总线上的报文  -s
        bus_rx = VectorBus(channel=channels[1], app_name=canAppName, bitrate=bitrate)
        listeners = [
            self.rx_callback
        ]
        notifier = can.Notifier(bus_rx, listeners)
        # 回调，实例化RX VectorBus，接收总线上的报文  -e

        # 实例化TX VectorBus（需要重新实例化），发送报文  -s
        bus_tx = VectorBus(channel=channels[0], app_name=canAppName, bitrate=bitrate)
        bus_tx.reset()  # activate channel
        msg = Message(is_extended_id=False, arbitration_id=id, data=data)  # 填充要发送的报文
        bus_tx.send(msg)  # 发送报文
        # 实例化TX VectorBus（需要重新实例化），发送报文  -e

        # 如果需要等待结果，则等待检测到期望报文(等待超时时长30s)  -s
        current_time = time.time()
        while self.validate_status and (time.time() - current_time <= timeout):
            time.sleep(0.1)
        # 如果需要等待结果，则等待检测到期望报文(等待超时时长30s)  -e

        notifier.stop()
        bus_rx.shutdown()
        bus_tx.shutdown()

        return self.response
