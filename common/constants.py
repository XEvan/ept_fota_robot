import os
import sys


class Constants:
    # 找到上一级目录，即根目录
    BASE_DIR = "D:/02_projects/07_vnxx/framework_robot"  # os.path.split(os.path.abspath(sys.argv[0]))[0]
    REPORT_BASE_DIR = os.path.join(BASE_DIR, "report_json")  # 保存json目录的路径
    REPORT_HTML_PATH = os.path.join(BASE_DIR, "report_html")  # 生成最终报告的路径
    LOG_BASE_DIR = os.path.join(BASE_DIR, "ept_logs")
    EACH_CASE_LOG = []  # 记录每一条测试用例的日志信息


if __name__ == '__main__':
    print("/".join(sys.path[0].split("\\")[:-1]))
