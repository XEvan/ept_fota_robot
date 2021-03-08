from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.channelbased_eth_controller import ChannelBasedEthController
from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.channelbased_can_controller import ChannelBasedCanController

'''
    底层接口管理
'''


class AwManager:
    xldriver_channelbased_eth_manager = ChannelBasedEthController()
    xldriver_channelbased_can_manager = ChannelBasedCanController()
