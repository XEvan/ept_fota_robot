"""
    通信过程中用到的全局变量
"""


class Constants:
    request_id = None

    @staticmethod
    def clean():
        """
        重置全局变量
        :return:
        """
        Constants.request_id = None
