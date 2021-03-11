import copy
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
        self.expected_can_id = 0x00  # 期望收到的can信号的id
        self.response = None

        self.blocksize = "00"  # blocksize，允许一次连续发送CF的数量

    def get_params_from_config(self):
        """
        从配置文件中获取配置信息
        :return:canAppName, channels, bitrate
        """
        # 获取配置文件中的配置信息  -s
        canAppName = str(self.canAppName.value, encoding="utf-8")  # CAN Application的name
        channels = []  # 配置文件中的CAN相关的AppChannel
        for name, ch in self.canAppChannel.items():
            channels.append(ch["appChannel"])
        bitrate = 500000
        # 获取配置文件中的配置信息  -e
        return canAppName, channels, bitrate

    def device_init(self, rx_handle):
        """
        生成一些操作对象:
            实例化TX
            实例化RX
        :return:
        """
        # 获取配置文件中的配置信息  -s
        canAppName, channels, bitrate = self.get_params_from_config()
        # 获取配置文件中的配置信息  -e

        # 回调，实例化RX VectorBus，接收总线上的报文  -s
        bus_rx = VectorBus(channel=channels[1], app_name=canAppName, bitrate=bitrate)
        listeners = [
            rx_handle  # rx的回调
        ]
        notifier = can.Notifier(bus_rx, listeners)
        # 回调，实例化RX VectorBus，接收总线上的报文  -e

        # 实例化TX VectorBus（需要重新实例化）  -s
        bus_tx = VectorBus(channel=channels[0], app_name=canAppName, bitrate=bitrate)
        bus_tx.reset()  # activate channel
        # 实例化TX VectorBus（需要重新实例化）  -e
        return bus_tx, bus_rx, notifier

    def driver_clean(self, bus_tx, bus_rx, notifier):
        notifier.stop()
        bus_rx.shutdown()
        bus_tx.shutdown()

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

    def wait_until(self, timeout=30):
        """
        等待超时
        :param timeout:
        :return:
        """
        # 如果需要等待结果，则等待检测到期望报文(等待超时时长30s)  -s
        current_time = time.time()
        while time.time() - current_time <= timeout:
            if not self.validate_status:  # 当self.validate_status为False的时候，表示已检测到或者不需要检测
                return True
            time.sleep(0.1)
        # 如果需要等待结果，则等待检测到期望报文(等待超时时长30s)  -e
        return False  # 超时

    def send_frame(self, obj, id, data):
        """
        发送can信号
        :param obj:
        :param id:
        :param data:
        :return:
        """
        msg = Message(is_extended_id=False, arbitration_id=id, data=data)  # 填充要发送的报文
        obj.send(msg)  # 发送报文

    def rx_single_callback(self, msg):
        """
        分析总线上的报文信息
        :param msg:
        :return:
        """
        if msg.arbitration_id == self.expected_can_id:
            self.validate_status = False  # 检测到期望报文
            self.response = msg

    def can_send_single_frame(self, id, data, wait_ret=True, expected_can_id=0x00, timeout=30):
        """
        单帧
        :param id: 发送的id
        :param data: 发送的数据
        :param wait_ret: 是否等待回复
        :return: 响应报文
        """
        self.validate_status = wait_ret  # 默认需要等待响应报文
        self.expected_can_id = expected_can_id  # 期望收到的CAN信号的id
        bus_tx, bus_rx, notifier = self.device_init(self.rx_single_callback)  # 初始化一些变量

        self.send_frame(bus_tx, id, data)  # 发送报文

        self.wait_until(timeout)  # 等待超时

        self.driver_clean(bus_tx, bus_rx, notifier)

        return True, self.response

    def str2bytes(self, s_str):
        """
        字符串转成字节
        0xF190->[f1, 90]
        :param s_str:
        :return:
        """
        s_str = str(hex(int(str(s_str), 10))[2:])[::-1]
        tmp = []
        i = 0
        while i < len(s_str):
            b_str = s_str[i:i + 2][::-1]
            b_str = "0%s" % b_str if len(b_str) < 2 else b_str
            tmp.append(int(b_str, 16))
            i += 2
        return tmp[::-1]

    def rx_multi_callback(self, msg):
        """
        分析总线上的报文信息
        :param msg:
        :return:
        """
        if msg.arbitration_id == self.expected_can_id:
            if msg.data[0] == 0x30:
                self.blocksize = hex(msg.data[1])[2:]  # 2 -> 0x02 ->"02"
                self.validate_status = False  # 检测到期望报文

            self.response = msg

    def can_send_multi_frame(self, id, sid, did, data, wait_ret=True, expected_can_id=0x00, timeout=30):
        """
        单帧
        :param id: 发送的id
        :param data: 发送的数据
        :param wait_ret: 是否等待回复
        :return: 响应报文
        """
        self.validate_status = wait_ret  # 默认需要等待响应报文
        self.expected_can_id = expected_can_id  # 期望收到的CAN信号的id
        bus_tx, bus_rx, notifier = self.device_init(self.rx_multi_callback)  # 初始化一些变量

        # 生成首帧，并发送  -s
        sid = self.str2bytes(sid)  # 0x2E -> [46(2E的十进制)]
        did = self.str2bytes(did)  # 0xF190 -> [241， 144]
        d_len = len(data) + 3  # sid*1+did*2=3
        data_1 = [0x10, d_len] + sid + did  # 10 14 2e

        first_frame_data = data_1 + data[:(8 - len(data_1))]  # 首帧报文

        self.send_frame(bus_tx, id, data)  # 发送报文

        res = self.wait_until(timeout)  # 超时时间内等待期望结果，如果没有等到，返回False
        if not res:
            self.driver_clean(bus_tx, bus_rx, notifier)
            return False
        # 生成首帧，并发送  -e

        # 生成后续的CF  -s
        left_data = data[(8 - len(data_1)):]
        round_num = self.blocksize[-1]  # 取blocksize的最后一位，为了给CF计数使用
        results = []  # 存放所有帧的数据
        tmp = []  # 临时存放每一帧的数据
        one = 1  # 计数器从1开始，直到F，下一个循环从0开始
        first_byte = None
        for i in range(len(left_data)):
            first_byte = int(round_num + str(one))  # 21, 22, 23, ..., 2F, 20, 21, 22
            first_byte = int(str(first_byte), 16)  # 转成十六进制
            tmp.append(left_data[i])
            if len(tmp) == 7:
                tmp = [first_byte] + tmp  # 拼接出完整的一帧
                results.append(copy.deepcopy(tmp))
                if one == 0xF:
                    one = 0  # 如果计数器达到了F，则从0开始
                else:
                    one += 1  # 每一帧加1
                tmp.clear()
        # tmp中可能还有剩余的元素
        if len(tmp) > 0:
            # first_byte = int(round_num + str(one))
            tmp = [first_byte] + tmp
            tmp += [0x55] * (8 - len(tmp))  # 不满8个的用55填充
            results.append(copy.deepcopy(tmp))  # 添加余下的元素
            tmp.clear()
        # 生成后续的CF  -e

        for cf in results:
            self.send_frame(bus_tx, id, cf)  # 剩余的CF连续发出去

        self.driver_clean(bus_tx, bus_rx, notifier)

        return True, self.response
