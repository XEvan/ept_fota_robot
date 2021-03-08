from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.channelbased_eth_rx import ChannelBasedEthRx
from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.channelbased_eth_tx import ChannelBasedEthTx


class ChannelBasedEthController(ChannelBasedEthTx, ChannelBasedEthRx):
    def __init__(self):
        super(ChannelBasedEthController, self).__init__()

    def activate_channel_handle(self):
        for _ in range(2):
            status = self.activate_channel(self.ethPortHandle, self.ethAccessMask, self.ethBusType)
            if status == 0:
                break
            if status == 118:  # XL_ERR_INVALID_PORT = 118
                self.close_port(self.ethPortHandle)
                self.open_port(self.ethAppName, self.ethPortHandle, self.ethAccessMask, self.ethPermissionMask,
                               self.ethBusType)


    def set_bypass_inactive_mode(self, source, target):
        """
            Eth下设置通道的bypass为inactive
        """
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        # 指定哪两个ETH的ByPass
        mask = self.ethAppChannel[source]["accessChannelMask"] | self.ethAppChannel[target]["accessChannelMask"]
        self.eth_set_bypass(self.ethPortHandle, mask, self.ethUserHandle, ChannelBasedConstants.XL_ETH_BYPASS_INACTIVE)

        self.activate_channel_handle()

    def set_bypass_mac_mode(self, source, target):
        """
            Eth下设置通道的bypass为 mac bypass
        """
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        # 指定哪两个ETH的ByPass
        mask = self.ethAppChannel[source]["accessChannelMask"] | self.ethAppChannel[target]["accessChannelMask"]
        self.eth_set_bypass(self.ethPortHandle, mask, self.ethUserHandle, ChannelBasedConstants.XL_ETH_BYPASS_MACCORE)
        self.activate_channel_handle()

    def driver_init(self):
        self.open_driver()
        self.set_appl_config(self.ethAppName, self.ethAppChannel, self.ethBusType)
        self.get_channel_mask(self.ethAppName, self.ethAppChannel, self.ethAccessMask, self.ethPermissionMask,
                              self.ethBusType)
        self.open_port(self.ethAppName, self.ethPortHandle, self.ethAccessMask, self.ethPermissionMask, self.ethBusType)

    def channel_setup(self):
        self.set_notification(self.ethPortHandle, self.ethNotificationHandle)
        self.set_bypass_init(self.ethPortHandle, self.ethUserHandle, self.ethAppChannel)  # 默认都设置成MAC BYPASS
        self.activate_channel_handle()

    def reset(self):
        '''
        初始化：两个步骤是连着的，固定的
        :return:
        '''
        self.init()
        self.driver_init()
        self.channel_setup()

    def cleanup(self):
        '''
        恢复初始设置：关闭端口和驱动
        :return:
        '''
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        self.close_port(self.ethPortHandle)
        self.close_driver()
